"""Type stubs for MANAGED_SWITCH category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .bounce_port import BouncePort
    from .cable_status import CableStatus
    from .faceplate_xml import FaceplateXml
    from .factory_reset import FactoryReset
    from .poe_reset import PoeReset
    from .port_stats_reset import PortStatsReset
    from .restart import Restart
    from .tx_rx import TxRx
    from .update import Update


class ManagedSwitch:
    """Type stub for ManagedSwitch."""

    bounce_port: BouncePort
    cable_status: CableStatus
    faceplate_xml: FaceplateXml
    factory_reset: FactoryReset
    poe_reset: PoeReset
    port_stats_reset: PortStatsReset
    restart: Restart
    tx_rx: TxRx
    update: Update

    def __init__(self, client: IHTTPClient) -> None: ...
