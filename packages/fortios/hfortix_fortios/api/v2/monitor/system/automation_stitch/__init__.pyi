"""Type stubs for AUTOMATION_STITCH category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .test import Test
    from .webhook import Webhook


class AutomationStitch:
    """Type stub for AutomationStitch."""

    test: Test
    webhook: Webhook

    def __init__(self, client: IHTTPClient) -> None: ...
