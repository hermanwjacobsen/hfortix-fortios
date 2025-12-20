"""
Internal Async HTTP Client for FortiOS API

This module contains the AsyncHTTPClient class which handles all async HTTP communication
with FortiGate devices. It mirrors HTTPClient but uses async/await with httpx.AsyncClient.

This is an internal implementation detail and not part of the public API.
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from typing import Any, Callable, Optional, TypeAlias, Union
from urllib.parse import quote

import httpx

from .http_client_base import BaseHTTPClient

logger = logging.getLogger("hfortix.http.async")

# Type alias for API responses
HTTPResponse: TypeAlias = dict[str, Any]

__all__ = ["AsyncHTTPClient", "HTTPResponse"]


class AsyncHTTPClient(BaseHTTPClient):
    """
    Internal async HTTP client for FortiOS API requests (Async Implementation)
    
    Implements the IHTTPClient protocol for asynchronous HTTP operations.

    Async version of HTTPClient using httpx.AsyncClient. Handles all HTTP communication
    with FortiGate devices including:
    - Async session management
    - Authentication headers
    - SSL verification
    - Request/response handling
    - Error handling
    - Automatic retry with exponential backoff
    - Async context manager support (use with 'async with' statement)

    Protocol Implementation:
        This class implements the IHTTPClient protocol, allowing it to be used
        interchangeably with other HTTP client implementations (e.g., HTTPClient,
        custom user-provided async clients). All methods return coroutines that
        must be awaited.

    This class is internal and not exposed to users directly, but users can provide
    their own async IHTTPClient implementations to FortiOS.__init__().
    """

    def __init__(
        self,
        url: str,
        verify: bool = True,
        token: Optional[str] = None,
        vdom: Optional[str] = None,
        max_retries: int = 3,
        connect_timeout: float = 10.0,
        read_timeout: float = 300.0,
        user_agent: Optional[str] = None,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: float = 60.0,
        max_connections: int = 100,
        max_keepalive_connections: int = 20,
    ) -> None:
        """
        Initialize async HTTP client

        Args:
            url: Base URL for API (e.g., "https://192.0.2.10")
            verify: Verify SSL certificates
            token: API authentication token
            vdom: Default virtual domain
            max_retries: Maximum number of retry attempts on transient failures (default: 3)
            connect_timeout: Timeout for establishing connection in seconds (default: 10.0)
            read_timeout: Timeout for reading response in seconds (default: 300.0)
            user_agent: Custom User-Agent header
            circuit_breaker_threshold: Number of consecutive failures before opening circuit (default: 5)
            circuit_breaker_timeout: Seconds to wait before transitioning to half-open (default: 60.0)
            max_connections: Maximum number of connections in the pool (default: 100)
            max_keepalive_connections: Maximum number of keepalive connections (default: 20)

        Raises:
            ValueError: If parameters are invalid
        """
        # Call parent class constructor (handles validation and common initialization)
        super().__init__(
            url=url,
            verify=verify,
            vdom=vdom,
            max_retries=max_retries,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            circuit_breaker_threshold=circuit_breaker_threshold,
            circuit_breaker_timeout=circuit_breaker_timeout,
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
        )

        # Set default User-Agent if not provided
        if user_agent is None:
            from . import __version__

            user_agent = f"hfortix/{__version__} (async)"

        # Initialize httpx AsyncClient
        self._client = httpx.AsyncClient(
            headers={"User-Agent": user_agent},
            timeout=httpx.Timeout(
                connect=connect_timeout,
                read=read_timeout,
                write=30.0,
                pool=10.0,
            ),
            verify=verify,
            http2=True,  # Enable HTTP/2 support
            limits=httpx.Limits(
                max_connections=max_connections, max_keepalive_connections=max_keepalive_connections
            ),
        )

        # Set token if provided
        if token:
            self._client.headers["Authorization"] = f"Bearer {token}"

        logger.debug(
            "Async HTTP client initialized for %s (max_retries=%d, connect_timeout=%.1fs, read_timeout=%.1fs, "
            "http2=enabled, user_agent='%s', circuit_breaker_threshold=%d, max_connections=%d)",
            self._url,
            max_retries,
            connect_timeout,
            read_timeout,
            user_agent,
            circuit_breaker_threshold,
            max_connections,
        )

    def get_connection_stats(self) -> dict[str, Any]:
        """Get connection statistics (placeholder for async)"""
        return {
            "active_connections": 0,  # httpx.AsyncClient doesn't expose this easily
            "idle_connections": 0,
        }

    def _handle_response_errors(self, response: httpx.Response) -> None:
        """Handle HTTP response errors using FortiOS error handling"""
        if not response.is_success:
            try:
                from .exceptions_forti import get_error_description, raise_for_status

                json_response = response.json()

                # Add error description if error code present
                error_code = json_response.get("error")
                if error_code and "error_description" not in json_response:
                    json_response["error_description"] = get_error_description(error_code)

                # Log the error
                status = json_response.get("status")
                http_status = json_response.get("http_status", response.status_code)
                error_desc = json_response.get("error_description", "Unknown error")

                logger.error(
                    "Request failed: HTTP %d, status=%s, error=%s, description='%s'",
                    http_status,
                    status,
                    error_code,
                    error_desc,
                )

                # Use FortiOS-specific error handling
                raise_for_status(json_response)

            except ValueError:
                logger.error(
                    "Request failed: HTTP %d (non-JSON response, %d bytes)",
                    response.status_code,
                    len(response.content),
                )
                response.raise_for_status()

    async def request(
        self,
        method: str,
        api_type: str,
        path: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None,
        raw_json: bool = False,
        request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Generic async request method for all API calls

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            api_type: API type (cmdb, monitor, log, service)
            path: API endpoint path
            data: Request body data (for POST/PUT)
            params: Query parameters dict
            vdom: Virtual domain
            raw_json: If False, return only 'results' field. If True, return full response
            request_id: Optional correlation ID for tracking requests

        Returns:
            dict: API response (results or full response based on raw_json)
        """
        # Generate request ID if not provided
        if request_id is None:
            request_id = str(uuid.uuid4())[:8]

        # Normalize and encode path
        path = self._normalize_path(path)
        encoded_path = quote(str(path), safe="/%") if isinstance(path, str) else path
        url = f"{self._url}/api/v2/{api_type}/{encoded_path}"
        params = params or {}

        # Handle vdom parameter
        if vdom is not None:
            params["vdom"] = vdom
        elif self._vdom is not None and "vdom" not in params:
            params["vdom"] = self._vdom

        # Build endpoint key
        full_path = f"/api/v2/{api_type}/{path}"
        endpoint_key = f"{api_type}/{path}"

        # Check circuit breaker
        try:
            self._check_circuit_breaker(endpoint_key)
        except RuntimeError as e:
            logger.error(
                "Circuit breaker blocked request",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "endpoint": full_path,
                    "circuit_state": self._circuit_breaker["state"],
                },
            )
            raise

        # Get endpoint-specific timeout if configured
        endpoint_timeout = self._get_endpoint_timeout(endpoint_key)

        # Log request start
        logger.debug(
            "Async request started",
            extra={
                "request_id": request_id,
                "method": method.upper(),
                "endpoint": full_path,
                "has_data": bool(data),
                "has_params": bool(params),
            },
        )

        # Track timing
        start_time = time.time()

        # Track total requests
        self._retry_stats["total_requests"] += 1

        # Retry loop with exponential backoff
        last_error = None
        for attempt in range(self._max_retries + 1):
            try:
                # Make async request
                res = await self._client.request(
                    method=method,
                    url=url,
                    json=data if data else None,
                    params=params if params else None,
                    timeout=endpoint_timeout if endpoint_timeout else None,
                )

                # Calculate duration
                duration = time.time() - start_time

                # Handle errors
                self._handle_response_errors(res)

                # Record success
                self._record_circuit_breaker_success()
                self._retry_stats["successful_requests"] += 1

                # Log successful response
                logger.info(
                    "Async request completed successfully",
                    extra={
                        "request_id": request_id,
                        "method": method.upper(),
                        "endpoint": full_path,
                        "status_code": res.status_code,
                        "duration_seconds": round(duration, 3),
                        "attempts": attempt + 1,
                    },
                )

                # Parse JSON response
                json_response = res.json()

                # Return based on raw_json flag
                if raw_json:
                    return json_response
                else:
                    return json_response.get("results", json_response)

            except Exception as e:
                last_error = e

                # Record failure
                self._record_circuit_breaker_failure(endpoint_key)

                # Check if we should retry
                if self._should_retry(e, attempt, endpoint_key):
                    response_obj = (
                        getattr(e, "response", None)
                        if isinstance(e, httpx.HTTPStatusError)
                        else None
                    )
                    delay = self._get_retry_delay(attempt, response_obj)

                    logger.info(
                        "Retrying async request after delay",
                        extra={
                            "request_id": request_id,
                            "method": method.upper(),
                            "endpoint": full_path,
                            "error_type": type(e).__name__,
                            "attempt": attempt + 1,
                            "max_attempts": self._max_retries + 1,
                            "delay_seconds": delay,
                        },
                    )

                    # Wait before retry (async sleep)
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise

        # If we've exhausted all retries
        if last_error:
            self._retry_stats["failed_requests"] += 1
            logger.error(
                "Async request failed after all retries",
                extra={
                    "request_id": request_id,
                    "method": method.upper(),
                    "endpoint": full_path,
                    "total_attempts": self._max_retries + 1,
                    "error_type": type(last_error).__name__,
                },
            )
            raise last_error

        raise RuntimeError("Request loop completed without success or error")

    async def get(
        self,
        api_type: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None,
        raw_json: bool = False,
    ) -> dict[str, Any]:
        """Async GET request"""
        return await self.request("GET", api_type, path, params=params, vdom=vdom, raw_json=raw_json)

    async def get_binary(
        self,
        api_type: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None,
    ) -> bytes:
        """Async GET request returning binary data"""
        path = path.lstrip("/") if isinstance(path, str) else path
        url = f"{self._url}/api/v2/{api_type}/{path}"
        params = params or {}

        # Add vdom
        if vdom is not None:
            params["vdom"] = vdom
        elif self._vdom is not None and "vdom" not in params:
            params["vdom"] = self._vdom

        # Make async request
        res = await self._client.get(url, params=params if params else None)

        # Handle errors
        self._handle_response_errors(res)

        return res.content

    async def post(
        self,
        api_type: str,
        path: str,
        data: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None,
        raw_json: bool = False,
    ) -> dict[str, Any]:
        """Async POST request - Create new object"""
        return await self.request(
            "POST", api_type, path, data=data, params=params, vdom=vdom, raw_json=raw_json
        )

    async def put(
        self,
        api_type: str,
        path: str,
        data: dict[str, Any],
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None,
        raw_json: bool = False,
    ) -> dict[str, Any]:
        """Async PUT request - Update existing object"""
        return await self.request(
            "PUT", api_type, path, data=data, params=params, vdom=vdom, raw_json=raw_json
        )

    async def delete(
        self,
        api_type: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        vdom: Optional[Union[str, bool]] = None,
        raw_json: bool = False,
    ) -> dict[str, Any]:
        """Async DELETE request - Delete object"""
        return await self.request("DELETE", api_type, path, params=params, vdom=vdom, raw_json=raw_json)

    # Validation helpers (same as sync - these are static methods)
    @staticmethod
    def validate_mkey(mkey: Any, parameter_name: str = "mkey") -> str:
        """Validate and convert mkey to string"""
        if mkey is None:
            raise ValueError(f"{parameter_name} is required and cannot be None")
        mkey_str = str(mkey).strip()
        if not mkey_str:
            raise ValueError(f"{parameter_name} cannot be empty")
        return mkey_str

    @staticmethod
    def validate_required_params(params: dict[str, Any], required: list[str]) -> None:
        """Validate that required parameters are present"""
        if not params:
            if required:
                raise ValueError(f"Missing required parameters: {', '.join(required)}")
            return
        missing = [param for param in required if param not in params or params[param] is None]
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")

    @staticmethod
    def validate_range(
        value: Union[int, float],
        min_val: Union[int, float],
        max_val: Union[int, float],
        parameter_name: str = "value",
    ) -> None:
        """Validate that a numeric value is within a specified range"""
        if not isinstance(value, (int, float)):
            raise ValueError(f"{parameter_name} must be a number")
        if not (min_val <= value <= max_val):
            raise ValueError(
                f"{parameter_name} must be between {min_val} and {max_val}, got {value}"
            )

    @staticmethod
    def validate_choice(value: Any, choices: list[Any], parameter_name: str = "value") -> None:
        """Validate that a value is one of the allowed choices"""
        if value not in choices:
            raise ValueError(f"{parameter_name} must be one of {choices}, got '{value}'")

    @staticmethod
    def build_params(**kwargs: Any) -> dict[str, Any]:
        """Build parameters dict, filtering out None values"""
        return {k: v for k, v in kwargs.items() if v is not None}

    async def __aenter__(self) -> "AsyncHTTPClient":
        """Async context manager entry"""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """Async context manager exit - ensures session is closed"""
        await self.close()

    async def close(self) -> None:
        """Close the async HTTP session and release resources"""
        if self._client:
            await self._client.aclose()
            logger.debug("Async HTTP client session closed")

    @staticmethod
    def make_exists_method(get_method: Callable[..., Any]) -> Callable[..., bool]:
        """
        Create an exists() helper that works with both sync and async modes.
        
        This utility wraps a get() method and returns a function that:
        - Returns True if the object exists
        - Returns False if ResourceNotFoundError is raised
        - Works transparently with both sync and async clients
        
        Args:
            get_method: The get() method to wrap (bound method from endpoint instance)
        
        Returns:
            A function that returns bool (sync) or Coroutine[bool] (async)
        
        Example:
            class Address:
                def __init__(self, client):
                    self._client = client
                
                def get(self, name, **kwargs):
                    return self._client.get("cmdb", f"/firewall/address/{name}", **kwargs)
                
                # Create exists method using the helper
                exists = AsyncHTTPClient.make_exists_method(get)
        """
        import inspect
        
        def exists_wrapper(*args: Any, **kwargs: Any) -> Union[bool, Any]:
            """Check if an object exists."""
            from hfortix.FortiOS.exceptions_forti import ResourceNotFoundError
            
            # Call the get method
            result = get_method(*args, **kwargs)
            
            # Check if we got a coroutine (async mode)
            if inspect.iscoroutine(result):
                # Return async version
                async def _exists_async():
                    try:
                        await result  # type: ignore[misc]
                        return True
                    except ResourceNotFoundError:
                        return False
                return _exists_async()
            else:
                # Sync mode - we already called get(), it succeeded
                # If it raised ResourceNotFoundError, we wouldn't be here
                return True
        
        return exists_wrapper
