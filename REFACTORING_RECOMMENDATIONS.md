# Refactoring Recommendations for HFortix

**Date:** December 20, 2025  
**Project:** HFortix v0.3.15+  
**Status:** Post-Interface Decoupling Analysis

This document provides actionable refactoring recommendations to improve code quality, reduce duplication, and enhance maintainability.

---

## 🔴 **CRITICAL: Code Duplication (Highest Priority)**

### 1. **Massive Duplication Between HTTPClient and AsyncHTTPClient**

**Problem:** ~90% of code is duplicated between sync and async HTTP clients (~1,200+ lines of identical logic)

**Duplicated Code:**
- Parameter validation (`__init__`)
- Data sanitization (`_sanitize_data`)
- Path normalization (`_normalize_path`)
- URL building (`_build_url`)
- Retry logic (`_should_retry`, `_get_retry_delay`)
- Circuit breaker logic (`_check_circuit_breaker`, `_record_circuit_breaker_*`)
- Statistics tracking (`_record_retry`, `get_retry_stats`, `get_circuit_breaker_state`)
- Error handling (`_handle_response_errors`)

**Impact:**
- Bug fixes must be applied twice
- Features must be implemented twice
- Testing burden doubled
- High maintenance cost
- Risk of divergence (sync and async behaving differently)

**Recommended Solution: Extract Shared Base Class**

Create `http_client_base.py`:

```python
"""
Shared HTTP Client Base Class

Contains all common logic for both sync and async HTTP clients.
"""

from __future__ import annotations

import fnmatch
import logging
import time
import uuid
from typing import Any, Optional, TypeAlias, Union
from urllib.parse import quote

import httpx

from .exceptions_forti import handle_fortigate_error

logger = logging.getLogger("hfortix.http.base")

HTTPResponse: TypeAlias = dict[str, Any]


class HTTPClientBase:
    """
    Base class for HTTP clients containing shared logic.
    
    This class contains all the common functionality between HTTPClient
    and AsyncHTTPClient, reducing code duplication and maintenance burden.
    
    Not meant to be instantiated directly - use HTTPClient or AsyncHTTPClient.
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
        """Initialize shared HTTP client components"""
        # Validate parameters (shared logic)
        self._validate_params(
            url, max_retries, connect_timeout, read_timeout,
            circuit_breaker_threshold, circuit_breaker_timeout,
            max_connections, max_keepalive_connections
        )
        
        # Store configuration
        self._url = url.rstrip("/")
        self._verify = verify
        self._vdom = vdom
        self._max_retries = max_retries
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._user_agent = user_agent or self._get_default_user_agent()
        
        # Initialize shared state
        self._retry_stats = self._init_retry_stats()
        self._circuit_breaker = self._init_circuit_breaker(
            circuit_breaker_threshold, circuit_breaker_timeout
        )
        self._endpoint_timeouts: dict[str, httpx.Timeout] = {}
    
    @staticmethod
    def _validate_params(
        url: str,
        max_retries: int,
        connect_timeout: float,
        read_timeout: float,
        circuit_breaker_threshold: int,
        circuit_breaker_timeout: float,
        max_connections: int,
        max_keepalive_connections: int,
    ) -> None:
        """Validate initialization parameters"""
        if not url:
            raise ValueError("URL is required")
        if max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if max_retries > 100:
            raise ValueError("max_retries cannot exceed 100")
        if connect_timeout <= 0:
            raise ValueError("connect_timeout must be positive")
        if read_timeout <= 0:
            raise ValueError("read_timeout must be positive")
        if circuit_breaker_threshold <= 0:
            raise ValueError("circuit_breaker_threshold must be positive")
        if circuit_breaker_timeout <= 0:
            raise ValueError("circuit_breaker_timeout must be positive")
        if max_connections <= 0:
            raise ValueError("max_connections must be positive")
        if max_keepalive_connections < 0:
            raise ValueError("max_keepalive_connections must be non-negative")
        if max_keepalive_connections > max_connections:
            raise ValueError(
                f"max_keepalive_connections ({max_keepalive_connections}) cannot exceed "
                f"max_connections ({max_connections})"
            )
    
    @staticmethod
    def _get_default_user_agent() -> str:
        """Get default User-Agent string"""
        try:
            from . import __version__
            return f"hfortix/{__version__}"
        except ImportError:
            return "hfortix/unknown"
    
    @staticmethod
    def _init_retry_stats() -> dict[str, Any]:
        """Initialize retry statistics dictionary"""
        return {
            "total_retries": 0,
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "retry_by_reason": {},
            "retry_by_endpoint": {},
            "last_retry_time": None,
        }
    
    @staticmethod
    def _init_circuit_breaker(threshold: int, timeout: float) -> dict[str, Any]:
        """Initialize circuit breaker state dictionary"""
        return {
            "consecutive_failures": 0,
            "last_failure_time": None,
            "state": "closed",
            "failure_threshold": threshold,
            "timeout": timeout,
        }
    
    @staticmethod
    def _sanitize_data(data: Optional[dict[str, Any]]) -> dict[str, Any]:
        """Sanitize request data by removing None values"""
        if data is None:
            return {}
        return {k: v for k, v in data.items() if v is not None}
    
    @staticmethod
    def _normalize_path(path: str) -> str:
        """Normalize API path by removing leading slash"""
        return path.lstrip("/") if isinstance(path, str) else path
    
    def _build_url(self, api_type: str, path: str) -> str:
        """Build complete API URL from components"""
        path = self._normalize_path(path)
        encoded_path = quote(str(path), safe="/%")
        return f"{self._url}/api/v2/{api_type}/{encoded_path}"
    
    def _record_retry(self, reason: str, endpoint: str) -> None:
        """Record retry attempt in statistics"""
        self._retry_stats["total_retries"] += 1
        self._retry_stats["last_retry_time"] = time.time()
        
        if reason not in self._retry_stats["retry_by_reason"]:
            self._retry_stats["retry_by_reason"][reason] = 0
        self._retry_stats["retry_by_reason"][reason] += 1
        
        if endpoint not in self._retry_stats["retry_by_endpoint"]:
            self._retry_stats["retry_by_endpoint"][endpoint] = 0
        self._retry_stats["retry_by_endpoint"][endpoint] += 1
    
    def _check_circuit_breaker(self, endpoint: str) -> None:
        """Check circuit breaker state before making request"""
        if self._circuit_breaker["state"] == "open":
            # Check if timeout has elapsed
            last_failure = self._circuit_breaker["last_failure_time"]
            timeout = self._circuit_breaker["timeout"]
            
            if last_failure and time.time() - last_failure < timeout:
                from .exceptions_forti import CircuitBreakerOpenError
                raise CircuitBreakerOpenError(
                    f"Circuit breaker is OPEN for {endpoint}. "
                    f"Wait {timeout} seconds before retrying."
                )
            else:
                # Transition to half-open
                self._circuit_breaker["state"] = "half_open"
                logger.info("Circuit breaker transitioned to HALF_OPEN")
    
    def _record_circuit_breaker_success(self) -> None:
        """Record successful request in circuit breaker"""
        if self._circuit_breaker["state"] == "half_open":
            self._circuit_breaker["state"] = "closed"
            self._circuit_breaker["consecutive_failures"] = 0
            logger.info("Circuit breaker transitioned to CLOSED")
        elif self._circuit_breaker["state"] == "closed":
            self._circuit_breaker["consecutive_failures"] = 0
    
    def _record_circuit_breaker_failure(self, endpoint: str) -> None:
        """Record failed request in circuit breaker"""
        self._circuit_breaker["consecutive_failures"] += 1
        self._circuit_breaker["last_failure_time"] = time.time()
        
        failures = self._circuit_breaker["consecutive_failures"]
        threshold = self._circuit_breaker["failure_threshold"]
        
        if failures >= threshold and self._circuit_breaker["state"] != "open":
            self._circuit_breaker["state"] = "open"
            logger.warning(
                f"Circuit breaker opened after {failures} consecutive failures on {endpoint}"
            )
    
    def _should_retry(self, error: Exception, attempt: int, endpoint: str = "") -> bool:
        """Determine if a request should be retried"""
        if attempt >= self._max_retries:
            return False
        
        # Retry on connection errors
        if isinstance(error, (httpx.ConnectError, httpx.NetworkError)):
            logger.debug(f"Retry {attempt + 1}/{self._max_retries}: Connection error")
            return True
        
        # Retry on timeouts
        if isinstance(error, (httpx.ReadTimeout, httpx.WriteTimeout, httpx.PoolTimeout)):
            logger.debug(f"Retry {attempt + 1}/{self._max_retries}: Timeout")
            return True
        
        # Retry on rate limits and server errors
        if isinstance(error, httpx.HTTPStatusError):
            status = error.response.status_code
            if status == 429:  # Rate limit
                logger.debug(f"Retry {attempt + 1}/{self._max_retries}: Rate limited")
                return True
            if status >= 500:  # Server errors
                logger.debug(f"Retry {attempt + 1}/{self._max_retries}: Server error {status}")
                return True
        
        return False
    
    def _get_retry_delay(self, attempt: int, response: Optional[httpx.Response] = None) -> float:
        """Calculate retry delay with exponential backoff"""
        # Check for Retry-After header
        if response is not None:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = float(retry_after)
                    logger.debug(f"Using Retry-After header: {delay}s")
                    return delay
                except ValueError:
                    pass
        
        # Exponential backoff: 1s, 2s, 4s, 8s, ... (capped at 30s)
        delay = min(2**attempt, 30.0)
        logger.debug(f"Exponential backoff delay: {delay}s")
        return delay
    
    def get_retry_stats(self) -> dict[str, Any]:
        """Get retry statistics"""
        total = self._retry_stats["total_requests"]
        successful = self._retry_stats["successful_requests"]
        success_rate = (successful / total * 100) if total > 0 else 0.0
        
        return {
            "total_retries": self._retry_stats["total_retries"],
            "total_requests": total,
            "successful_requests": successful,
            "failed_requests": self._retry_stats["failed_requests"],
            "retry_by_reason": self._retry_stats["retry_by_reason"].copy(),
            "retry_by_endpoint": self._retry_stats["retry_by_endpoint"].copy(),
            "last_retry_time": self._retry_stats["last_retry_time"],
            "success_rate": success_rate,
        }
    
    def get_circuit_breaker_state(self) -> dict[str, Any]:
        """Get current circuit breaker state"""
        return self._circuit_breaker.copy()
    
    def _handle_response_errors(self, response: httpx.Response) -> None:
        """Handle HTTP response errors using FortiOS error handling"""
        if not response.is_success:
            handle_fortigate_error(response.status_code, response.text)
```

Then update HTTPClient and AsyncHTTPClient to inherit:

```python
# http_client.py
class HTTPClient(HTTPClientBase):
    """Synchronous HTTP client implementation"""
    
    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)
        
        # Sync-specific: Initialize httpx.Client
        self._client = httpx.Client(
            headers={"User-Agent": self._user_agent},
            timeout=httpx.Timeout(...),
            verify=self._verify,
            http2=True,
            limits=httpx.Limits(...)
        )
        
        if kwargs.get('token'):
            self._client.headers["Authorization"] = f"Bearer {kwargs['token']}"
    
    def request(self, method: str, api_type: str, path: str, **kwargs) -> dict:
        # Sync-specific request logic
        # Uses self._should_retry(), self._get_retry_delay(), etc. from base
        ...
```

```python
# http_client_async.py
class AsyncHTTPClient(HTTPClientBase):
    """Asynchronous HTTP client implementation"""
    
    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)
        
        # Async-specific: Initialize httpx.AsyncClient
        self._client = httpx.AsyncClient(
            headers={"User-Agent": self._user_agent},
            timeout=httpx.Timeout(...),
            verify=self._verify,
            http2=True,
            limits=httpx.Limits(...)
        )
        
        if kwargs.get('token'):
            self._client.headers["Authorization"] = f"Bearer {kwargs['token']}"
    
    async def request(self, method: str, api_type: str, path: str, **kwargs) -> dict:
        # Async-specific request logic
        # Uses self._should_retry(), self._get_retry_delay(), etc. from base
        ...
```

**Estimated Effort:** 8-12 hours  
**Impact:** Reduces codebase by ~600 lines, eliminates 90% duplication  
**Priority:** HIGH - Should be done before v1.0

---

## 🟡 **HIGH: Endpoint Code Duplication**

### 2. **Repetitive Parameter Handling in Endpoints**

**Problem:** Every endpoint method has identical boilerplate:

```python
# Repeated ~2000+ times across endpoints
params = payload_dict.copy() if payload_dict else {}
data_payload = payload_dict.copy() if payload_dict else {}
```

**Recommended Solution: Helper Methods**

Create `endpoint_utils.py`:

```python
"""Utility functions for endpoint classes"""

from typing import Any, Optional

def prepare_params(payload_dict: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Prepare parameters dictionary for API call"""
    return payload_dict.copy() if payload_dict else {}

def prepare_data(payload_dict: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Prepare data payload dictionary for API call"""
    return payload_dict.copy() if payload_dict else {}
```

Then update endpoints:

```python
# Before
params = payload_dict.copy() if payload_dict else {}

# After
from ....endpoint_utils import prepare_params
params = prepare_params(payload_dict)
```

**Estimated Effort:** 4-6 hours (can be scripted)  
**Impact:** Reduces code by ~1,000 lines, centralizes logic  
**Priority:** MEDIUM - Nice cleanup for v1.1

---

### 3. **Repetitive Endpoint Path Building**

**Problem:** Every method builds paths the same way:

```python
# Repeated hundreds of times
if name:
    endpoint = f"/firewall/address/{name}"
else:
    endpoint = "/firewall/address"
```

**Recommended Solution: Path Builder Method**

Add to `HTTPClientBase`:

```python
def build_endpoint_path(self, base_path: str, identifier: Optional[str] = None) -> str:
    """Build endpoint path with optional identifier"""
    if identifier:
        return f"{base_path}/{identifier}"
    return base_path
```

Then update endpoints:

```python
# Before
if name:
    endpoint = f"/firewall/address/{name}"
else:
    endpoint = "/firewall/address"

# After
endpoint = self._client.build_endpoint_path("/firewall/address", name)
```

**Estimated Effort:** 6-8 hours (script + testing)  
**Impact:** Cleaner code, centralized path logic  
**Priority:** LOW - Minor improvement

---

## 🟢 **MEDIUM: Type Hints & Documentation**

### 4. **Inconsistent Return Type Annotations**

**Problem:** Some methods have incomplete type hints:

```python
# Inconsistent
def exists(self, name: str, vdom: str | bool | None = None):
    # Should specify return type

# Better
def exists(self, name: str, vdom: str | bool | None = None) -> bool | Any:
    # Returns bool in sync, Coroutine[bool] in async
```

**Recommended Solution: Add Complete Type Hints**

Create a typing module for common patterns:

```python
# types.py
from typing import Any, Coroutine, TypeAlias, Union

# Type for methods that work in both sync and async
SyncOrAsync: TypeAlias = Union[dict[str, Any], Coroutine[Any, Any, dict[str, Any]]]
BoolOrAsync: TypeAlias = Union[bool, Coroutine[Any, Any, bool]]
```

Then use consistently:

```python
from ....types import BoolOrAsync

def exists(self, name: str, vdom: str | bool | None = None) -> BoolOrAsync:
    """Check if object exists (works in sync and async modes)"""
    ...
```

**Estimated Effort:** 4-6 hours  
**Impact:** Better IDE support, fewer type errors  
**Priority:** MEDIUM - Good for v0.4 or v1.0

---

## 🔵 **LOW: Code Organization**

### 5. **Long Method Signatures in Endpoints**

**Problem:** Some methods have 40+ parameters:

```python
def post(
    self,
    payload_dict: dict[str, Any] | None = None,
    param1: str | None = None,
    param2: str | None = None,
    # ... 38 more parameters ...
    param40: str | None = None,
    vdom: str | bool | None = None,
    raw_json: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
```

**Recommended Solution: Accept Dict or Kwargs**

For endpoints with many parameters, prefer dict-based API:

```python
def post(
    self,
    data: dict[str, Any] | None = None,
    *,
    vdom: str | bool | None = None,
    raw_json: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """
    Create new object.
    
    Args:
        data: Object configuration (all parameters as dict)
        vdom: Virtual domain
        raw_json: Return full response
        **kwargs: Alternative - pass parameters as keyword arguments
    
    Examples:
        # Dict style
        fgt.api.cmdb.firewall.address.post(data={
            "name": "test",
            "subnet": "10.0.0.1/32",
            # ... 40 more fields
        })
        
        # Kwargs style (same result)
        fgt.api.cmdb.firewall.address.post(
            name="test",
            subnet="10.0.0.1/32",
            # ... 40 more fields
        )
    """
    # Merge data and kwargs
    final_data = data.copy() if data else {}
    final_data.update(kwargs)
    
    return self._client.post("cmdb", "/firewall/address", data=final_data, vdom=vdom, raw_json=raw_json)
```

**Estimated Effort:** 12-16 hours (affects many files)  
**Impact:** Cleaner method signatures, more Pythonic  
**Priority:** LOW - Breaking change, consider for v2.0

---

### 6. **Hardcoded API Types**

**Problem:** API types ("cmdb", "monitor", etc.) are hardcoded strings:

```python
return self._client.get("cmdb", endpoint, ...)
```

**Recommended Solution: Enum for API Types**

```python
# constants.py
from enum import Enum

class APIType(str, Enum):
    """FortiOS API types"""
    CMDB = "cmdb"
    MONITOR = "monitor"
    LOG = "log"
    SERVICE = "service"
```

Then use:

```python
from ....constants import APIType

return self._client.get(APIType.CMDB, endpoint, ...)
```

**Estimated Effort:** 3-4 hours  
**Impact:** Prevents typos, better autocomplete  
**Priority:** LOW - Nice to have

---

## 🎯 **PERFORMANCE: Optimization Opportunities**

### 7. **Unnecessary Dict Copies**

**Problem:** Many unnecessary `.copy()` calls:

```python
# Creates 2 copies
params = payload_dict.copy() if payload_dict else {}
# Later...
final_params = params.copy()
```

**Recommended Solution: Copy Only When Needed**

```python
# Use dict directly if not modified
params = payload_dict or {}

# Only copy if you modify it
if need_to_modify:
    params = (payload_dict or {}).copy()
    params['extra'] = value
```

**Estimated Effort:** 2-3 hours (automated)  
**Impact:** Minor performance improvement  
**Priority:** LOW - Micro-optimization

---

### 8. **String Formatting in Hot Paths**

**Problem:** F-strings in loop-heavy code:

```python
# Called thousands of times
logger.debug(f"Request {i}/{total}")
```

**Recommended Solution: Lazy Logging**

```python
# Only formats if debug level is enabled
logger.debug("Request %d/%d", i, total)
```

**Estimated Effort:** 1-2 hours  
**Impact:** Faster execution when logging disabled  
**Priority:** LOW - Minor optimization

---

## 🧪 **TESTING: Test Infrastructure**

### 9. **Missing Unit Test Infrastructure**

**Problem:** No unit tests for shared logic (from DEBT-002)

**Recommended Solution: pytest + fixtures**

```python
# tests/conftest.py
import pytest
from hfortix import FortiOS

@pytest.fixture
def mock_client():
    """Mock HTTP client for testing"""
    class MockHTTPClient:
        def get(self, api_type, path, **kwargs):
            return {"status": "success", "results": []}
        def post(self, api_type, path, data, **kwargs):
            return {"status": "success"}
        # ... put, delete
    return MockHTTPClient()

@pytest.fixture
def fgt_sync(mock_client):
    """Sync FortiOS instance with mock client"""
    return FortiOS(client=mock_client, mode="sync")

@pytest.fixture
def fgt_async(mock_client):
    """Async FortiOS instance with mock client"""
    return FortiOS(client=mock_client, mode="async")
```

**Estimated Effort:** 40-60 hours (comprehensive coverage)  
**Impact:** Catch bugs early, safe refactoring  
**Priority:** HIGH - Must have for v1.0

---

## 📋 **Summary & Priorities**

### Immediate (v0.4 - Next 2-4 weeks)
1. ✅ **Extract HTTPClientBase** (8-12h) - Eliminates 90% duplication
2. ✅ **Add endpoint_utils.py** (4-6h) - Cleans up repetitive code

### Before v1.0 (Next 2-3 months)
3. ✅ **Complete type hints** (4-6h) - Better IDE support
4. ✅ **Unit test infrastructure** (40-60h) - Critical for stability
5. ✅ **Add constants.py** (3-4h) - Prevents typos

### v2.0 Considerations (6+ months)
6. ⏸️ **Simplify method signatures** (12-16h) - Breaking change
7. ⏸️ **Path builder refactor** (6-8h) - Minor cleanup

### Optional Optimizations
8. ⏸️ **Remove unnecessary copies** (2-3h) - Micro-optimization
9. ⏸️ **Lazy logging** (1-2h) - Micro-optimization

---

## 🎬 **Quick Wins (Do First)**

These can be done quickly with high impact:

1. **Create endpoint_utils.py** (2 hours)
   - `prepare_params()` and `prepare_data()` helpers
   - Immediate cleanup of 750+ files

2. **Add constants.py** (1 hour)
   - `APIType` enum
   - Prevents typos in API type strings

3. **Extract _sanitize_data to base** (30 minutes)
   - Move to HTTPClientBase
   - Test both clients still work

4. **Add type aliases** (1 hour)
   - Create types.py with SyncOrAsync, BoolOrAsync
   - Better type hints across endpoints

---

## 📝 **Implementation Notes**

### For HTTPClientBase Extraction:
- Start with static methods (_sanitize_data, _normalize_path)
- Move validation logic next
- Then statistics and circuit breaker
- Finally retry logic
- Test each step thoroughly

### For endpoint_utils.py:
- Create helpers first
- Write script to update all files
- Test a few endpoints manually
- Run full update script
- Verify with type checker

### For Testing:
- Start with HTTPClientBase tests
- Then HTTPClient and AsyncHTTPClient tests
- Add endpoint tests last
- Aim for 80%+ coverage

---

## 🚀 **Estimated Total Effort**

- **Critical refactoring:** 12-18 hours
- **High priority:** 48-66 hours
- **Medium priority:** 8-12 hours
- **Total for v1.0:** 68-96 hours (~2-3 weeks)

---

**Next Steps:**
1. Review this document with team
2. Prioritize which refactorings to include in v0.4
3. Create GitHub issues for tracking
4. Begin with HTTPClientBase extraction (highest impact)
5. Follow up with endpoint_utils.py (quick win)

**Questions? Concerns?**
- Is the HTTPClientBase approach acceptable?
- Should we do these refactorings before or after v1.0?
- Any other pain points to address?
