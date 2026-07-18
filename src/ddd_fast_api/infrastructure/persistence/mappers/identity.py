"""Mapping helpers for identity persistence models."""

from ddd_fast_api.domain.identity import EmailAddress, UserAccount, UserAccountStatus
from ddd_fast_api.infrastructure.persistence.models import UserAccountModel


def to_domain_user_account(model: UserAccountModel) -> UserAccount:
    """Translate an ORM model into the identity domain entity."""

    return UserAccount(
        id=model.id,
        email=EmailAddress(model.email),
        display_name=model.display_name,
        status=UserAccountStatus(model.status),
    )
