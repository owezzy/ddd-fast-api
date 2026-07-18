"""Identity domain value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmailAddress:
    """Normalized email address for user identity."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not normalized:
            raise ValueError("Email address cannot be empty.")
        if "@" not in normalized:
            raise ValueError("Email address must contain '@'.")
        local_part, domain = normalized.split("@", maxsplit=1)
        if not local_part or not domain or "." not in domain:
            raise ValueError("Email address must contain a valid domain.")

        object.__setattr__(self, "value", normalized)
