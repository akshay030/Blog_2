from fastapi import APIRouter,status,Depends,Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.users.schemas import UserResponseSchema,UserSchema,LoginSchema,LoginResponseSchema,IsAuthResponseSchema
from src.users import controllers
from src.utils.helper import is_authenticated
from src.users.models import UserModel
from src.utils.limiter import limiter
user_routes=APIRouter(prefix='/user',tags=["Users"])


@user_routes.post('/register',response_model=UserResponseSchema,status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def register(request: Request,body:UserSchema,db:Session=Depends(get_db)):
    return controllers.register(body,db)

@user_routes.post('/login',response_model=LoginResponseSchema,status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def login(request: Request,body:LoginSchema,db:Session=Depends(get_db)):
    return controllers.login(body,db)


@user_routes.get(
    "/is_auth",
    response_model=IsAuthResponseSchema,
    status_code=status.HTTP_200_OK
)
def is_auth(
    user: UserModel = Depends(is_authenticated)
):
    return {
        "authenticated": True,
        "user": user
    }
    
@user_routes.post("/logout")
def logout(
    user: UserModel = Depends(is_authenticated)
):
    return controllers.logout(user)