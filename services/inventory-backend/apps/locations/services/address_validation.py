from dataclasses import dataclass
from typing import Protocol


@dataclass
class AddressValidationResult:
    status: str
    confidence: int | None = None
    provider_reference: str = ""
    message: str = ""
    payload: dict | None = None


class AddressValidationProvider(Protocol):
    provider_name: str

    def validate(self, raw_address: str) -> AddressValidationResult:
        ...


class LocalCatalogValidationProvider:
    provider_name = "local"

    def validate(self, raw_address: str) -> AddressValidationResult:
        # Placeholder implementation for MVP:
        # parse/normalize is handled in-platform and matched against local catalog.
        return AddressValidationResult(
            status="parsed",
            confidence=75,
            message="Local catalog placeholder validation.",
            payload={"raw_input": raw_address},
        )


class GoogleAddressValidationProvider:
    provider_name = "google"

    def validate(self, raw_address: str) -> AddressValidationResult:
        # Placeholder for post-MVP external provider integration.
        return AddressValidationResult(
            status="skipped",
            message="Google validation not configured.",
            payload={"raw_input": raw_address},
        )


class USPSAddressValidationProvider:
    provider_name = "usps"

    def validate(self, raw_address: str) -> AddressValidationResult:
        # Placeholder for post-MVP external provider integration.
        return AddressValidationResult(
            status="skipped",
            message="USPS validation not configured.",
            payload={"raw_input": raw_address},
        )
