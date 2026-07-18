"""SQLAlchemy-backed repository for the identity slice."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_fast_api.domain.identity import EmailAddress, IdentityRepository, UserAccount
from ddd_fast_api.infrastructure.persistence.mappers import to_domain_user_account
from ddd_fast_api.infrastructure.persistence.models import UserAccountModel


class SQLAlchemyIdentityRepository(IdentityRepository):
    """Concrete identity repository using SQLAlchemy async sessions."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_account_by_email(self, email: EmailAddress) -> UserAccount | None:
        result = await self.session.execute(
            select(UserAccountModel).where(UserAccountModel.email == email.value),
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_domain_user_account(model)
