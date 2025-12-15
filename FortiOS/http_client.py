"""
Internal HTTP Client for FortiOS API

This module contains the HTTPClient class which handles all HTTP communication
with FortiGate devices. It is an internal implementation detail and not part
of the public API.
"""
from __future__ import annotations

from typing import Any, Optional, Union

import requests


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
