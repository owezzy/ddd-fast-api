"""Tests for identity application use cases."""

from dataclasses import dataclass

import pytest

from ddd_fast_api.application.identity import GetUserAccountByEmail
from ddd_fast_api.domain.identity import EmailAddress, UserAccount


@dataclass(slots=True)
class InMemoryIdentityRepository:
    accounts: list[UserAccount]

    async def get_account_by_email(self, email: EmailAddress) -> UserAccount | None:
        for account in self.accounts:
            if account.email == email:
                return account
        return None


@pytest.mark.anyio
async def test_get_user_account_by_email_returns_matching_account() -> None:
    account = UserAccount(
        id="user-1",
        email=EmailAddress("user@example.com"),
        display_name="Starter user",
    )
    use_case = GetUserAccountByEmail(repository=InMemoryIdentityRepository(accounts=[account]))

    result = await use_case.execute(EmailAddress("USER@example.com"))

    assert result == account


@pytest.mark.anyio
async def test_get_user_account_by_email_returns_none_when_missing() -> None:
    use_case = GetUserAccountByEmail(repository=InMemoryIdentityRepository(accounts=[]))

    result = await use_case.execute(EmailAddress("missing@example.com"))

    assert result is None
