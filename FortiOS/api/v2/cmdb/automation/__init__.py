"""
FortiOS CMDB - Automation API

This module provides access to FortiOS automation configuration endpoints.
"""

from .setting import Setting


class Automation:
    """Automation configuration endpoints"""
    
    def __init__(self, client):
        """
        Initialize Automation API
        
        Args:
            client: FortiOS client instance
        """
        self._client = client
        
        # Initialize endpoint classes
        self.setting = Setting(client)
