#!/usr/bin/env python3
"""
Script to update all endpoint files to use IHTTPClient protocol instead of HTTPClient.

This updates:
1. Import statements: HTTPClient -> IHTTPClient
2. Type hints in __init__: client: 'HTTPClient' -> client: 'IHTTPClient'
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def find_endpoint_files(base_path: Path) -> List[Path]:
    """Find all endpoint Python files in the FortiOS/api directory."""
    api_path = base_path / "hfortix" / "FortiOS" / "api"
    if not api_path.exists():
        raise FileNotFoundError(f"API path not found: {api_path}")
    
    endpoint_files = []
    for root, dirs, files in os.walk(api_path):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                endpoint_files.append(Path(root) / file)
    
    return endpoint_files


def update_file_content(file_path: Path) -> Tuple[bool, str]:
    """
    Update a single file's content.
    
    Returns:
        Tuple of (was_modified, status_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        # Update import statements
        # Pattern 1: from ....http_client import HTTPClient
        # Pattern 2: from .....http_client import HTTPClient
        # etc.
        import_pattern = r'from (\.+)http_client import HTTPClient'
        if re.search(import_pattern, content):
            content = re.sub(import_pattern, r'from \1http_client_interface import IHTTPClient', content)
            modified = True
        
        # Update type hints in __init__ methods
        # Pattern: def __init__(self, client: 'HTTPClient'
        init_pattern = r"def __init__\(self, client: ['\"]HTTPClient['\"]"
        if re.search(init_pattern, content):
            content = re.sub(init_pattern, "def __init__(self, client: 'IHTTPClient'", content)
            modified = True
        
        # Update any direct HTTPClient type references in the class
        # Pattern: self._client: HTTPClient or similar
        type_hint_pattern = r': [\'"]?HTTPClient[\'"]?'
        # But be careful not to replace in comments or strings
        # This is a simple approach - we'll verify manually
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Updated"
        else:
            return False, "No changes needed"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    """Main execution function."""
    base_path = Path(__file__).parent
    
    print("Finding endpoint files...")
    try:
        endpoint_files = find_endpoint_files(base_path)
        print(f"Found {len(endpoint_files)} endpoint files")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    if not endpoint_files:
        print("No endpoint files found!")
        return
    
    # Ask for confirmation before proceeding
    print("\nThis will update:")
    print("  - Import statements: HTTPClient -> IHTTPClient")
    print("  - Type hints: client: 'HTTPClient' -> client: 'IHTTPClient'")
    print(f"\nTotal files to process: {len(endpoint_files)}")
    
    response = input("\nProceed? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Aborted.")
        return
    
    print("\nProcessing files...")
    modified_count = 0
    error_count = 0
    
    for i, file_path in enumerate(endpoint_files, 1):
        was_modified, status = update_file_content(file_path)
        
        if "Error" in status:
            error_count += 1
            print(f"[{i}/{len(endpoint_files)}] ERROR: {file_path.relative_to(base_path)}: {status}")
        elif was_modified:
            modified_count += 1
            if modified_count <= 10:  # Show first 10 updates
                print(f"[{i}/{len(endpoint_files)}] ✓ {file_path.relative_to(base_path)}")
        
        # Show progress every 50 files
        if i % 50 == 0:
            print(f"Progress: {i}/{len(endpoint_files)} files processed...")
    
    print("\n" + "="*60)
    print(f"Processing complete!")
    print(f"  Total files: {len(endpoint_files)}")
    print(f"  Modified: {modified_count}")
    print(f"  Unchanged: {len(endpoint_files) - modified_count - error_count}")
    print(f"  Errors: {error_count}")
    print("="*60)
    
    if modified_count > 0:
        print("\nNext steps:")
        print("  1. Review changes: git diff")
        print("  2. Run type checker: mypy FortiOS/")
        print("  3. Run tests to verify backward compatibility")


if __name__ == "__main__":
    main()
