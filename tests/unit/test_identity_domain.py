"""Tests for the initial identity domain skeleton."""

import pytest

from ddd_fast_api.domain.identity import EmailAddress, UserAccount, UserAccountStatus


def test_email_address_normalizes_to_lowercase() -> None:
    email = EmailAddress(" Alice@example.COM ")

    assert email.value == "alice@example.com"


@pytest.mark.parametrize(
    ("raw_value", "message"),
    [
        ("", "Email address cannot be empty."),
        ("alice", "Email address must contain '@'."),
        ("alice@localhost", "Email address must contain a valid domain."),
    ],
)
def test_email_address_rejects_invalid_values(raw_value: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        EmailAddress(raw_value)


def test_user_account_requires_meaningful_display_name() -> None:
    with pytest.raises(ValueError, match="Display name must contain at least 3 characters."):
        UserAccount(id="user-1", email=EmailAddress("user@example.com"), display_name=" a ")


def test_user_account_lifecycle_toggles_status() -> None:
    account = UserAccount(
        id="user-1",
        email=EmailAddress("user@example.com"),
        display_name="Starter user",
    )

    assert account.is_active is True
    assert account.status is UserAccountStatus.ACTIVE

    account.disable()

    assert account.is_active is False
    assert account.status is UserAccountStatus.DISABLED

    account.activate()

    assert account.is_active is True
    assert account.status is UserAccountStatus.ACTIVE
