"""
FortiOS CMDB Diameter Filter API
Diameter filter configuration endpoints
"""


class DiameterFilter:
    """
    Diameter Filter API helper class
    Provides access to diameter-filter configuration endpoints
    """
    
    def __init__(self, client):
        """
        Initialize Diameter Filter helper
        
        Args:
            client: FortiOS client instance
        """
        self._client = client
        
        # Initialize endpoint classes
        from .profile import Profile
        
        self.profile = Profile(client)
