"""Identity domain repository ports."""

from __future__ import annotations

from typing import Protocol

from ddd_fast_api.domain.identity.entities import UserAccount
from ddd_fast_api.domain.identity.value_objects import EmailAddress


class IdentityRepository(Protocol):
    """Port for retrieving user accounts."""

    async def get_account_by_email(self, email: EmailAddress) -> UserAccount | None:
        """Return a user account by email, if it exists."""
