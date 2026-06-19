from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.helper import is_authenticated
from src.comments.schemas import CommentResponseSchema, CommentSchema
from src.users.models import UserModel
from src.comments import controllers
from fastapi import status
from typing import List
import uuid

comments_routes = APIRouter(prefix="/blogs", tags=["Comments"])


@comments_routes.post(
    "/{blog_id}",
    response_model=CommentResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def add_comment(
    blog_id: uuid.UUID,
    body: CommentSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):

    return controllers.add_comment(blog_id, body, db, user)


@comments_routes.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: UserModel = Depends(is_authenticated),
):
    return controllers.delete_comment(comment_id, db, user)


@comments_routes.get(
    "/{blog_id}/comments",
    response_model=List[CommentResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_comments_by_blog_id(blog_id: uuid.UUID, db: Session = Depends(get_db)):
    return controllers.get_comments_by_blog_id(blog_id, db)
