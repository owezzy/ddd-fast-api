"""Identity domain entities."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ddd_fast_api.domain.identity.value_objects import EmailAddress


class UserAccountStatus(StrEnum):
    """Lifecycle status for a user account."""

    ACTIVE = "active"
    DISABLED = "disabled"


@dataclass(slots=True)
class UserAccount:
    """Identity entity for a local user account."""

    id: str
    email: EmailAddress
    display_name: str
    status: UserAccountStatus = UserAccountStatus.ACTIVE

    def __post_init__(self) -> None:
        normalized_name = self.display_name.strip()
        if not self.id.strip():
            raise ValueError("User account id cannot be empty.")
        if len(normalized_name) < 3:
            raise ValueError("Display name must contain at least 3 characters.")

        self.id = self.id.strip()
        self.display_name = normalized_name

    def disable(self) -> None:
        self.status = UserAccountStatus.DISABLED

    def activate(self) -> None:
        self.status = UserAccountStatus.ACTIVE

    @property
    def is_active(self) -> bool:
        return self.status is UserAccountStatus.ACTIVE
