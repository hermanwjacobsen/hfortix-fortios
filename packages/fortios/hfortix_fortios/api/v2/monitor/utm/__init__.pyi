"""Type stubs for UTM category."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hfortix_core.http.interface import IHTTPClient
    from .antivirus import Antivirus
    from .app_lookup import AppLookup
    from .application_categories import ApplicationCategories
    from .blacklisted_certificates import BlacklistedCertificates
    from .rating_lookup import RatingLookup


class Utm:
    """Type stub for Utm."""

    rating_lookup: RatingLookup
    antivirus: Antivirus
    app_lookup: AppLookup
    application_categories: ApplicationCategories
    blacklisted_certificates: BlacklistedCertificates

    def __init__(self, client: IHTTPClient) -> None: ...
