from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from typing import TYPE_CHECKING
from fastapi import Depends
from Sql_Models.classes import get_access_token_db
bearer_transport = BearerTransport(
    tokenUrl='auth/jwt/login'
)
if TYPE_CHECKING:
    from Sql_Models.classes import AccessToken
def get_database_strategy(
    access_token_db: AccessTokenDatabase['AccessToken'] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db, 
        lifetime_seconds=3600
        )


auth_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)