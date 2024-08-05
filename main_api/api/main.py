from fastapi import FastAPI, Depends
from main_api.api.routers import router1
from fastapi_users import fastapi_users, FastAPIUsers
from all_models.orm_models.classess import user
from main_api.auth.backauth import auth_backend
from main_api.auth.schemas import UserCreate,UserRead, UserUpdate
from main_api.auth.manager import get_user_manager




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

@app.get("/protected_route")
def protected_route(user: user = Depends(fastapi_users.current_user(active=True, verified=True))):
    return f'{user.id}'