from typing import TYPE_CHECKING
from typing import Optional
from typing import AsyncGenerator
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from all_models.orm_models.classess import AccessToken, user, async_session_maker


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator['AsyncSession', None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: 'AsyncSession' = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, user)


async def get_access_token_db(
    session: 'AsyncSession' = Depends(get_async_session),
):  
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)



class UserManager(IntegerIDMixin, BaseUserManager[user, int]):
    reset_password_token_secret = '6be99a4bd4dcec5f15dc2fd2f9caa82a04273bda04a7af551645dedd22ea132c'
    verification_token_secret = 'e9d73ff9763da91388bbef9c6703152527f8c6f9f91a84b94887e9318aba376f'


    async def on_after_register(self, user: user, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


    async def on_after_forgot_password(
        self, user: user, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: user, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


