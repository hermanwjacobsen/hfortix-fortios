from __future__ import annotations

from typing import Any, Optional, Union

import requests

__all__ = ['FortiOS']


class HTTPClient:
    """
    Internal HTTP client for FortiOS API requests
    
    Handles all HTTP communication with FortiGate devices including:
    - Session management
    - Authentication headers
    - SSL verification
    - Request/response handling
    - Error handling
    
    This class is internal and not exposed to users.
    """
    
    def __init__(
        self,
        url: str,
        verify: bool = True,
        token: Optional[str] = None,
        vdom: Optional[str] = None
    ) -> None:
        """
        Initialize HTTP client
        
        Args:
            url: Base URL for API (e.g., "https://192.0.2.10")
            verify: Verify SSL certificates
            token: API authentication token
            vdom: Default virtual domain
        """
        self._url = url
        self._verify = verify
        self._vdom = vdom
        self._session = requests.Session()
        self._session.verify = verify
        
        if not verify:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Set token if provided
        if token:
            self._session.headers['Authorization'] = f'Bearer {token}'
    
    def _handle_response_errors(self, response: requests.Response) -> None:
        """
        Handle HTTP response errors consistently

        Args:
            response: requests.Response object

        Raises:
            APIError: If response contains JSON error details
            HTTPError: If response is not JSON (via raise_for_status)
        """
        if not response.ok:
            try:
                error_detail = response.json()
                from .exceptions import APIError
                raise APIError(
                    f"HTTP {response.status_code}: {error_detail}"
                )
            except ValueError:
                # If response is not JSON, raise standard HTTP error
                response.raise_for_status()
    
    def request(
        self,
        method: str,
        api_type: str,
        path: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None
    ) -> dict[str, Any]:
        """
        Generic request method for all API calls

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            api_type: API type (cmdb, monitor, log, service)
            path: API endpoint path (e.g., 'firewall/address', 'system/status')
            data: Request body data (for POST/PUT)
            params: Query parameters dict
            vdom: Virtual domain (None=use default, or specify vdom name)

        Returns:
            JSON response
        """
        url = f"{self._url}/api/v2/{api_type}/{path}"
        params = params or {}

        # Only add vdom parameter if explicitly specified
        if vdom is not None:
            params['vdom'] = vdom
        elif self._vdom is not None and 'vdom' not in params:
            params['vdom'] = self._vdom

        # Make request
        res = self._session.request(
            method=method,
            url=url,
            json=data if data else None,
            params=params if params else None
        )

        # Handle errors
        self._handle_response_errors(res)

        return res.json()
    
    def get(
        self,
        api_type: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None
    ) -> dict[str, Any]:
        """GET request"""
        return self.request('GET', api_type, path, params=params, vdom=vdom)
    
    def get_binary(
        self,
        api_type: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None
    ) -> bytes:
        """
        GET request returning binary data (for file downloads)
        
        Args:
            api_type: API type
            path: Endpoint path
            params: Query parameters
            vdom: Virtual domain
        
        Returns:
            Raw binary response data
        """
        url = f"{self._url}/api/v2/{api_type}/{path}"
        params = params or {}

        # Add vdom if applicable
        if vdom is not None:
            params['vdom'] = vdom
        elif self._vdom is not None and 'vdom' not in params:
            params['vdom'] = self._vdom

        # Make request
        res = self._session.get(url, params=params if params else None)

        # Handle errors
        self._handle_response_errors(res)

        return res.content
    
    def post(
        self,
        api_type: str,
        path: str,
        data: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None
    ) -> dict[str, Any]:
        """POST request - Create new object"""
        return self.request('POST', api_type, path, data=data, params=params, vdom=vdom)
    
    def put(
        self,
        api_type: str,
        path: str,
        data: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None
    ) -> dict[str, Any]:
        """PUT request - Update existing object"""
        return self.request('PUT', api_type, path, data=data, params=params, vdom=vdom)
    
    def delete(
        self,
        api_type: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None
    ) -> dict[str, Any]:
        """DELETE request - Delete object"""
        return self.request('DELETE', api_type, path, params=params, vdom=vdom)
    
    def close(self) -> None:
        """Close the HTTP session and release resources"""
        if self._session:
            self._session.close()


class FortiOS:
    """
    FortiOS REST API Client
    
    Python client for interacting with Fortinet FortiGate firewalls via REST API.
    Supports configuration management (CMDB), monitoring, logging, and services.
    
    This client uses token-based authentication and provides a stateless interface
    to FortiOS devices. No login/logout required - just initialize with your token
    and start making API calls.
    
    Main API categories:
        - api.cmdb: Configuration Management Database (firewall policies, objects, etc.)
        - api.monitor: Real-time monitoring and status
        - api.log: Log queries and analysis
        - api.service: System services (sniffer, security rating, etc.)
    
    Attributes:
        api (API): API namespace containing cmdb, monitor, log, service
    
    Example:
        >>> from fortinet import FortiOS
        >>> fgt = FortiOS("fortigate.example.com", token="your_token_here")
        >>> 
        >>> # List firewall addresses
        >>> addresses = fgt.api.cmdb.firewall.address.list()
        >>> 
        >>> # Create a firewall address
        >>> fgt.api.cmdb.firewall.address.create(
        ...     name='test-host',
        ...     subnet='192.0.2.100/32',
        ...     comment='Example host'
        ... )
        >>> 
        >>> # Get system status
        >>> status = fgt.api.monitor.system.status.get()
    
    Note:
        - Requires FortiOS 6.0+ with REST API enabled
        - API token must be created in FortiOS: System > Admin > API Users
        - Use verify=False only in development with self-signed certificates
    
    See Also:
        - API Reference: https://docs.fortinet.com/
        - Token Setup: QUICKSTART.md
        - Examples: EXAMPLES.md
    """
    
    def __init__(
        self,
        host: Optional[str] = None,
        token: Optional[str] = None,
        verify: bool = True,
        vdom: Optional[str] = None,
        port: Optional[int] = None
    ) -> None:
        """
        Initialize FortiOS API client

        With token authentication, everything is stateless - just provide credentials
        and start making API calls. No login/logout needed.

        Args:
            host: FortiGate IP/hostname (e.g., "192.0.2.10" or "fortigate.example.com")
            token: API token for authentication
            verify: Verify SSL certificates (default: True, recommended for production)
            vdom: Virtual domain (default: None = FortiGate's default VDOM)
            port: HTTPS port (default: None = use 443, or specify custom port like 8443)

        Examples:
            # Production - with valid SSL certificate
            fgt = FortiOS("fortigate.example.com", token="your_token_here", verify=True)

            # Development/Testing - with self-signed certificate (example IP from RFC 5737)
            fgt = FortiOS("192.0.2.10", token="your_token_here", verify=False)

            # Custom port
            fgt = FortiOS("192.0.2.10", token="your_token_here", verify=False, port=8443)

            # Port in hostname (alternative)
            fgt = FortiOS("192.0.2.10:8443", token="your_token_here", verify=False)
        """
        self._host = host
        self._vdom = vdom
        self._port = port

        # Build URL with port handling
        if host:
            # If port is already in host string, use as-is
            if ':' in host:
                url = f"https://{host}"
            # If explicit port provided, append it
            elif port:
                url = f"https://{host}:{port}"
            # Otherwise use default (443)
            else:
                url = f"https://{host}"
        else:
            url = None

        # Initialize HTTP client
        self._client = HTTPClient(
            url=url,
            verify=verify,
            token=token,
            vdom=vdom
        )

        # Initialize API namespace
        from .api import API
        
        self.api = API(self._client)

    def __dir__(self):
        """Control autocomplete to show only public attributes"""
        return ['api']

    @property
    def host(self) -> Optional[str]:
        """FortiGate hostname or IP address"""
        return self._host

    @property
    def port(self) -> Optional[int]:
        """HTTPS port number"""
        return self._port

    @property
    def vdom(self) -> Optional[str]:
        """Active virtual domain"""
        return self._vdom

    def close(self) -> None:
        """
        Close the HTTP session and release resources

        Optional: Python automatically cleans up when object is destroyed.
        Use this for explicit resource management or in long-running apps.
        """
        self._client.close()

    def __enter__(self) -> 'FortiOS':
        """Context manager entry"""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Context manager exit - automatically closes session"""
        self.close()
        return False

