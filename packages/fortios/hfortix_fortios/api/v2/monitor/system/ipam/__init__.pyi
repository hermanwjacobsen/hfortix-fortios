"""Type stubs for IPAM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .utilization import Utilization


class Ipam:
    """Type stub for Ipam."""

    utilization: Utilization

    def __init__(self, client: IHTTPClient) -> None: ...
