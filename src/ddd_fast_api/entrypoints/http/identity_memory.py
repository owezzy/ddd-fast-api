"""Temporary in-memory adapter for the sample identity endpoint."""

from __future__ import annotations

from dataclasses import dataclass, field

from ddd_fast_api.domain.identity import EmailAddress, IdentityRepository, UserAccount


@dataclass(slots=True)
class InMemoryIdentityRepository(IdentityRepository):
    """Edge-layer adapter supplying sample identity data."""

    accounts: list[UserAccount] = field(default_factory=list)

    async def get_account_by_email(self, email: EmailAddress) -> UserAccount | None:
        for account in self.accounts:
            if account.email == email:
                return account
        return None


def build_sample_identity_repository() -> InMemoryIdentityRepository:
    """Create the temporary sample identity dataset for the scaffold."""

    return InMemoryIdentityRepository(
        accounts=[
            UserAccount(
                id="user-1",
                email=EmailAddress("user@example.com"),
                display_name="Starter user",
            ),
        ],
    )
