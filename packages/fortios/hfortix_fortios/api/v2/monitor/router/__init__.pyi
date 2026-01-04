"""Type stubs for ROUTER category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .charts import Charts
    from .ipv4 import Ipv4
    from .ipv6 import Ipv6
    from .lookup_policy import LookupPolicy
    from .ospf import Ospf
    from .policy import Policy
    from .policy6 import Policy6
    from .sdwan import Sdwan
    from .statistics import Statistics
    from .bgp import Bgp
    from .lookup import Lookup


class Router:
    """Type stub for Router."""

    bgp: Bgp
    lookup: Lookup
    charts: Charts
    ipv4: Ipv4
    ipv6: Ipv6
    lookup_policy: LookupPolicy
    ospf: Ospf
    policy: Policy
    policy6: Policy6
    sdwan: Sdwan
    statistics: Statistics

    def __init__(self, client: IHTTPClient) -> None: ...
