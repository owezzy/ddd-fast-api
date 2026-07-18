"""Identity application use cases."""

from __future__ import annotations

from dataclasses import dataclass

from ddd_fast_api.domain.identity import EmailAddress, IdentityRepository, UserAccount


@dataclass(slots=True)
class GetUserAccountByEmail:
    """Read-only use case for retrieving a user account by email."""

    repository: IdentityRepository

    async def execute(self, email: EmailAddress) -> UserAccount | None:
        return await self.repository.get_account_by_email(email)
