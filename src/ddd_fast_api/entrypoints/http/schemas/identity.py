"""Transport schemas for identity endpoints."""

from pydantic import BaseModel

from ddd_fast_api.domain.identity import UserAccount, UserAccountStatus


class UserAccountResponse(BaseModel):
    """Boundary model for user accounts returned by the API."""

    id: str
    email: str
    display_name: str
    status: UserAccountStatus

    @classmethod
    def from_domain(cls, account: UserAccount) -> "UserAccountResponse":
        return cls(
            id=account.id,
            email=account.email.value,
            display_name=account.display_name,
            status=account.status,
        )
