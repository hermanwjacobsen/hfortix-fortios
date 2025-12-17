"""
FortiOS CMDB - Router Category

Router configuration endpoints for routing protocols and settings.

Endpoints:
    - access_list: IPv4 access lists
    - access_list6: IPv6 access lists
    - aspath_list: AS path lists
    - auth_path: Authentication-based routing
    - bfd: BFD configuration
    - bfd6: IPv6 BFD configuration
    - bgp: BGP configuration
    - community_list: BGP community lists
    - extcommunity_list: Extended community lists
    - isis: IS-IS configuration
    - key_chain: Key chain configuration
    - multicast: Multicast routing
    - multicast_flow: Multicast flow
    - multicast6: IPv6 multicast routing
    - ospf: OSPF configuration
    - ospf6: IPv6 OSPF configuration
    - policy: IPv4 routing policies
    - policy6: IPv6 routing policies
    - prefix_list: IPv4 prefix lists
    - prefix_list6: IPv6 prefix lists
    - rip: RIP configuration
    - ripng: RIPng configuration
    - route_map: Route maps
    - setting: Router settings
    - static: IPv4 static routes
    - static6: IPv6 static routes
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....http_client import HTTPClient

__all__ = ["Router"]


class Router:
    """Router category endpoint class"""

    def __init__(self, client: "HTTPClient") -> None:
        """
        Initialize Router category

        Args:
            client: HTTPClient instance
        """
        self._client = client

    @property
    def access_list(self):
        """Access IPv4 access lists endpoint"""
        from .access_list import AccessList
        return AccessList(self._client)

    @property
    def access_list6(self):
        """Access IPv6 access lists endpoint"""
        from .access_list6 import AccessList6
        return AccessList6(self._client)

    @property
    def aspath_list(self):
        """Access AS path lists endpoint"""
        from .aspath_list import AspathList
        return AspathList(self._client)

    @property
    def auth_path(self):
        """Access authentication-based routing endpoint"""
        from .auth_path import AuthPath
        return AuthPath(self._client)

    @property
    def bfd(self):
        """Access BFD configuration endpoint"""
        from .bfd import Bfd
        return Bfd(self._client)

    @property
    def bfd6(self):
        """Access IPv6 BFD configuration endpoint"""
        from .bfd6 import Bfd6
        return Bfd6(self._client)

    @property
    def bgp(self):
        """Access BGP configuration endpoint"""
        from .bgp import Bgp
        return Bgp(self._client)

    @property
    def community_list(self):
        """Access BGP community lists endpoint"""
        from .community_list import CommunityList
        return CommunityList(self._client)

    @property
    def extcommunity_list(self):
        """Access extended community lists endpoint"""
        from .extcommunity_list import ExtcommunityList
        return ExtcommunityList(self._client)

    @property
    def isis(self):
        """Access IS-IS configuration endpoint"""
        from .isis import Isis
        return Isis(self._client)

    @property
    def key_chain(self):
        """Access key chain configuration endpoint"""
        from .key_chain import KeyChain
        return KeyChain(self._client)

    @property
    def multicast(self):
        """Access multicast routing endpoint"""
        from .multicast import Multicast
        return Multicast(self._client)

    @property
    def multicast_flow(self):
        """Access multicast flow endpoint"""
        from .multicast_flow import MulticastFlow
        return MulticastFlow(self._client)

    @property
    def multicast6(self):
        """Access IPv6 multicast routing endpoint"""
        from .multicast6 import Multicast6
        return Multicast6(self._client)

    @property
    def ospf(self):
        """Access OSPF configuration endpoint"""
        from .ospf import Ospf
        return Ospf(self._client)

    @property
    def ospf6(self):
        """Access OSPFv3 configuration endpoint"""
        from .ospf6 import Ospf6
        return Ospf6(self._client)

    @property
    def policy(self):
        """Access IPv4 routing policies endpoint"""
        from .policy import Policy
        return Policy(self._client)

    @property
    def policy6(self):
        """Access IPv6 routing policies endpoint"""
        from .policy6 import Policy6
        return Policy6(self._client)

    @property
    def prefix_list(self):
        """Access IPv4 prefix lists endpoint"""
        from .prefix_list import PrefixList
        return PrefixList(self._client)

    @property
    def prefix_list6(self):
        """Access IPv6 prefix lists endpoint"""
        from .prefix_list6 import PrefixList6
        return PrefixList6(self._client)

    @property
    def rip(self):
        """Access RIP configuration endpoint"""
        from .rip import Rip
        return Rip(self._client)

    @property
    def ripng(self):
        """Access RIPng configuration endpoint"""
        from .ripng import Ripng
        return Ripng(self._client)

    @property
    def route_map(self):
        """Access route maps endpoint"""
        from .route_map import RouteMap
        return RouteMap(self._client)

    @property
    def setting(self):
        """Access router settings endpoint"""
        from .setting import Setting
        return Setting(self._client)

    @property
    def static(self):
        """Access IPv4 static routes endpoint"""
        from .static import Static
        return Static(self._client)

    @property
    def static6(self):
        """Access IPv6 static routes endpoint"""
        from .static6 import Static6
        return Static6(self._client)
