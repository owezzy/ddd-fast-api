"""Catalog domain value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SKU:
    """Stock-keeping unit identifier for a catalog item."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()
        if not normalized:
            raise ValueError("SKU cannot be empty.")
        if len(normalized) < 3:
            raise ValueError("SKU must contain at least 3 characters.")
        if any(not (char.isalnum() or char == "-") for char in normalized):
            raise ValueError("SKU may contain only letters, numbers, and hyphens.")

        object.__setattr__(self, "value", normalized)
