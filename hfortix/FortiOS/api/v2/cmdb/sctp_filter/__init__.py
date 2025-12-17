"""
FortiOS CMDB - SCTP Filter Category

SCTP (Stream Control Transmission Protocol) filter configuration.

Endpoints:
    - profile: SCTP filter profiles
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ....http_client import HTTPClient

__all__ = ["SctpFilter"]


class SctpFilter:
    """SCTP Filter category endpoint class"""

    def __init__(self, client: "HTTPClient") -> None:
        """
        Initialize SCTP Filter category

        Args:
            client: HTTPClient instance
        """
        self._client = client

    @property
    def profile(self):
        """Access SCTP filter profiles endpoint"""
        from .profile import Profile
        return Profile(self._client)
