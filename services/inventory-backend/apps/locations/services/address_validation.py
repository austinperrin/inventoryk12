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

    def validate(self, raw_address: str) -> AddressValidationResult: ...


class InternalAddressValidationProvider:
    provider_name = "internal"

    def validate(self, raw_address: str) -> AddressValidationResult:
        return AddressValidationResult(
            status="parsed",
            confidence=75,
            message="Internal parser/catalog validation baseline.",
            payload={"raw_input": raw_address},
        )
