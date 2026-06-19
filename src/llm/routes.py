from fastapi import APIRouter, Depends
from fastapi import status


from src.llm.schemas import (
    GenerateBlogSchema,
    GenerateBlogResponse,
)
from src.utils.permissions import require_roles
from src.users.models import UserRole, UserModel
from src.llm import controllers

ai_routes = APIRouter(prefix="/ai", tags=["AI"])


@ai_routes.post(
    "/generate-blog",
    response_model=GenerateBlogResponse,
    status_code=status.HTTP_200_OK,
)
def generate_blog(
    body: GenerateBlogSchema,
    user: UserModel = Depends(require_roles(UserRole.AUTHOR, UserRole.ADMIN)),
):
    return controllers.generate_blog(body)
