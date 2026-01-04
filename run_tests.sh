#!/bin/bash
# Run CMDB tests with optimal parallelization
#
# Usage:
#   ./run_tests.sh                    # Run all tests
#   ./run_tests.sh validators         # Run only validator tests (fast)
#   ./run_tests.sh api                # Run only API tests (slow)
#   ./run_tests.sh firewall           # Run tests for specific category

set -e

cd "$(dirname "$0")"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get number of CPU cores
CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

case "${1:-all}" in
    validators|val)
        echo -e "${BLUE}🚀 Running validator tests in parallel (${CORES} workers)${NC}"
        .venv/bin/python -m pytest .tests/pytests/api/cmdb/ \
            -m "validator" \
            -n "$CORES" \
            --tb=line \
            -v
        ;;
    
    api)
        echo -e "${YELLOW}🔄 Running API tests serially (one at a time)${NC}"
        .venv/bin/python -m pytest .tests/pytests/api/cmdb/ \
            -m "api_call" \
            --tb=line \
            -v
        ;;
    
    all)
        echo -e "${BLUE}🧪 Running all tests with smart parallelization${NC}"
        echo -e "   - Validators: ${CORES} parallel workers"
        echo -e "   - API calls: Sequential execution"
        echo ""
        .venv/bin/python -m pytest .tests/pytests/api/cmdb/ \
            -n "$CORES" \
            --tb=line \
            -v
        ;;
    
    *)
        # Run tests for specific path/category
        echo -e "${BLUE}🧪 Running tests for: ${1}${NC}"
        .venv/bin/python -m pytest ".tests/pytests/api/cmdb/${1}" \
            -n "$CORES" \
            --tb=line \
            -v
        ;;
esac

echo -e "${GREEN}✅ Tests complete!${NC}"
