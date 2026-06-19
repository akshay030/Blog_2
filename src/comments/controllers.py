from src.comments.models import CommentModel
from src.comments.schemas import CommentSchema
from src.users.models import UserModel,UserRole
from src.blogs.models import BlogModel
from fastapi import HTTPException, status
import json
from src.utils.redis import redis_client
from sqlalchemy.orm import Session
import uuid


def get_comments_by_blog_id(blog_id: uuid.UUID, db: Session):

    cache_key = f"comments:{blog_id}"

    cached_comments = redis_client.get(cache_key)

    if cached_comments:

        return json.loads(cached_comments)

    blog = db.get(BlogModel, blog_id)

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    comments = db.query(CommentModel).filter(CommentModel.blog_id == blog_id).all()

    comments_data = [
        {
            "id": str(comment.id),
            "comment": comment.comment,
            "name": comment.name,
            "blog_id": str(comment.blog_id),
            "user_id": str(comment.user_id),
            "created_at": comment.created_at.isoformat(),
            "updated_at": comment.updated_at.isoformat(),
        }
        for comment in comments
    ]

    redis_client.set(cache_key, json.dumps(comments_data), ex=300)

    return comments_data


def add_comment(blog_id: uuid.UUID, body: CommentSchema, db: Session, user: UserModel):
    blog = db.get(BlogModel, blog_id)

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )

    new_comment = CommentModel(
        comment=body.comment, blog_id=blog_id, user_id=user.id, name=user.name
    )

    db.add(new_comment)
    db.commit()
    redis_client.delete(f"comments:{blog_id}")
    db.refresh(new_comment)

    return new_comment


def delete_comment(id: uuid.UUID, db: Session, user: UserModel):
    comment = db.get(CommentModel, id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    if user.role != UserRole.ADMIN:
        if comment.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this comment",
            )
    blog_id = comment.blog_id

    db.delete(comment)
    db.commit()
    redis_client.delete(f"comments:{blog_id}")
    return {"message": "Comment deleted successfully"}
