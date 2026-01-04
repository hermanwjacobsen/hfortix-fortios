"""Type stubs for BGP category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .clear_soft_in import ClearSoftIn
    from .clear_soft_out import ClearSoftOut
    from .soft_reset_neighbor import SoftResetNeighbor


class Bgp:
    """Type stub for Bgp."""

    clear_soft_in: ClearSoftIn
    clear_soft_out: ClearSoftOut
    soft_reset_neighbor: SoftResetNeighbor

    def __init__(self, client: IHTTPClient) -> None: ...
