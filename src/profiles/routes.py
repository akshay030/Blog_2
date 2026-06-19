from fastapi import APIRouter, Depends
from src.profiles.schemas import ProfileResponseSchema, UpdateProfileSchema
from src.users.models import UserModel
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.helper import is_authenticated
from src.profiles import controllers

profile_routes = APIRouter(prefix="/profile", tags=["Profile"])


@profile_routes.get("/me", response_model=ProfileResponseSchema)
def get_profile(
    db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)
):
    return controllers.get_my_profile(db, user)


@profile_routes.put("/edit", response_model=ProfileResponseSchema)
def edit_profile(
    body: UpdateProfileSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controllers.edit_profile(body, db, user)
