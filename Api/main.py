from fastapi import FastAPI, APIRouter, Depends
from Api.routes import router1
from fastapi_users import fastapi_users, FastAPIUsers
from Dao.orm_models.classess import user
from auth.backauth import auth_backend
from auth.schemas import UserCreate,UserRead, UserUpdate
from auth.manager import get_user_manager

from fastapi.security import HTTPBearer



app = FastAPI()

fastapi_users = FastAPIUsers[user, int](
    get_user_manager,
    [auth_backend],
)

@app.get('/')
def start():
    return 'todo app'


app.include_router(router1)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)