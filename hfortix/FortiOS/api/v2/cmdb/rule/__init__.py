"""
FortiOS CMDB - Rule Category

Rule signature endpoints for various detection systems.

Endpoints:
    - fmwp: FortiManager Wireless Protection signatures
    - iotd: IOT detection signatures
    - otdt: OT (Operational Technology) detection signatures
    - otvp: OT patch signatures
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....http_client import HTTPClient

__all__ = ["Rule"]


class Rule:
    """Rule category endpoint class"""

    def __init__(self, client: "HTTPClient") -> None:
        """
        Initialize Rule category

        Args:
            client: HTTPClient instance
        """
        self._client = client

    @property
    def fmwp(self):
        """Access FMWP signatures endpoint"""
        from .fmwp import Fmwp
        return Fmwp(self._client)

    @property
    def iotd(self):
        """Access IOT detection signatures endpoint"""
        from .iotd import Iotd
        return Iotd(self._client)

    @property
    def otdt(self):
        """Access OT detection signatures endpoint"""
        from .otdt import Otdt
        return Otdt(self._client)

    @property
    def otvp(self):
        """Access OT patch signatures endpoint"""
        from .otvp import Otvp
        return Otvp(self._client)
