"""Type stubs for SDN_CONNECTOR category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .update import Update
    from .validate_gcp_key import ValidateGcpKey


class SdnConnector:
    """Type stub for SdnConnector."""

    update: Update
    validate_gcp_key: ValidateGcpKey

    def __init__(self, client: IHTTPClient) -> None: ...
