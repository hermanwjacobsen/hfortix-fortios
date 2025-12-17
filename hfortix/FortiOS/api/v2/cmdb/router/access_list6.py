"""
FortiOS CMDB - Router Access List6

Configure IPv6 access lists.

API Endpoints:
    GET    /api/v2/cmdb/router/access-list6        - List all IPv6 access lists
    GET    /api/v2/cmdb/router/access-list6/{name} - Get specific IPv6 access list
    POST   /api/v2/cmdb/router/access-list6        - Create IPv6 access list
    PUT    /api/v2/cmdb/router/access-list6/{name} - Update IPv6 access list
    DELETE /api/v2/cmdb/router/access-list6/{name} - Delete IPv6 access list
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from hfortix.FortiOS.http_client import encode_path_component

if TYPE_CHECKING:
    from ....http_client import HTTPClient


class AccessList6:
    """Router IPv6 access list endpoint"""

    def __init__(self, client: "HTTPClient") -> None:
        """
        Initialize Router Access List6 endpoint

        Args:
            client: HTTPClient instance
        """
        self._client = client

    def list(self, vdom: Optional[Union[str, bool]] = None, **kwargs: Any) -> dict[str, Any]:
        """List all IPv6 access lists."""
        return self.get(vdom=vdom, **kwargs)

    def get(
        self,
        name: Optional[str] = None,
        vdom: Optional[Union[str, bool]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Get IPv6 access list(s)."""
        path = "router/access-list6"
        if name:
            path = f"{path}/{encode_path_component(name)}"
        return self._client.get("cmdb", path, params=kwargs if kwargs else None, vdom=vdom)

    def create(
        self,
        data_dict: Optional[dict[str, Any]] = None,
        name: Optional[str] = None,
        comments: Optional[str] = None,
        rule: Optional[list] = None,
        vdom: Optional[Union[str, bool]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create IPv6 access list."""
        data = data_dict.copy() if data_dict else {}
        if name is not None:
            data["name"] = name
        if comments is not None:
            data["comments"] = comments
        if rule is not None:
            data["rule"] = rule
        data.update(kwargs)
        return self._client.post("cmdb", "router/access-list6", data=data, vdom=vdom)

    def update(
        self,
        name: str,
        data_dict: Optional[dict[str, Any]] = None,
        comments: Optional[str] = None,
        rule: Optional[list] = None,
        vdom: Optional[Union[str, bool]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update IPv6 access list."""
        data = data_dict.copy() if data_dict else {}
        if comments is not None:
            data["comments"] = comments
        if rule is not None:
            data["rule"] = rule
        data.update(kwargs)
        path = f"router/access-list6/{encode_path_component(name)}"
        return self._client.put("cmdb", path, data=data, vdom=vdom)

    def delete(self, name: str, vdom: Optional[Union[str, bool]] = None) -> dict[str, Any]:
        """Delete IPv6 access list."""
        path = f"router/access-list6/{encode_path_component(name)}"
        return self._client.delete("cmdb", path, vdom=vdom)

    def exists(self, name: str, vdom: Optional[Union[str, bool]] = None) -> bool:
        """Check if IPv6 access list exists."""
        try:
            self.get(name=name, vdom=vdom)
            return True
        except Exception:
            return False
