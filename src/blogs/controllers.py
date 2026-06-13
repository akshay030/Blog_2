
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from src.blogs.models import BlogModel
from src.blogs.schemas import BlogSchema,UpdateBlogSchema,BlogResponseSchema
from src.users.models import UserModel,UserRole
import uuid
from src.utils.redis import redis_client
import json


def create_blog(body:BlogSchema,db:Session,user:UserModel):
    new_blog = BlogModel(
    title=body.title,
    introduction=body.introduction,
    content=body.content,
    conclusion=body.conclusion,

    slug=body.slug,
    meta_description=body.meta_description,
    keywords=body.keywords,

    user_id=user.id
)
    
    db.add(new_blog)
    db.commit()
    redis_client.delete("blogs")
    db.refresh(new_blog)
    return new_blog
    
def get_all_blogs(db:Session):
    cached_blogs = redis_client.get("blogs")

    if cached_blogs:

        print("CACHE HIT")

        return json.loads(cached_blogs)

    print("CACHE MISS")
    blogs  = db.query(BlogModel).all()
    
    blogs_data = [
    BlogResponseSchema.model_validate(
        blog
    ).model_dump(mode="json")
    for blog in blogs
]
    redis_client.set(
        "blogs",
        json.dumps(blogs_data),
        ex=300
    )

    return blogs_data

def get_blog_by_id(
    id: uuid.UUID,
    db: Session
):

    cache_key = f"blog:{id}"

    cached_blog = redis_client.get(
        cache_key
    )

    if cached_blog:

        print("BLOG CACHE HIT")

        return json.loads(cached_blog)

    print("BLOG CACHE MISS")

    blog = db.get(BlogModel, id)

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )

    blog_data = {
        "id": str(blog.id),
        "title": blog.title,
        "introduction": blog.introduction,
        "content": blog.content,
        "conclusion": blog.conclusion,

        "slug": blog.slug,
        "meta_description": blog.meta_description,
        "keywords": blog.keywords or [],

        "user_id": str(blog.user_id),

        "created_at": blog.created_at.isoformat(),
        "updated_at": blog.updated_at.isoformat(),
    }

    redis_client.set(
        cache_key,
        json.dumps(blog_data),
        ex=300
    )

    return blog_data

def update_blog(id: uuid.UUID, body: UpdateBlogSchema, db: Session,user:UserModel):
    blog = db.get(BlogModel, id)

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    if user.role != UserRole.ADMIN:

        if blog.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not allowed")

    update_data = body.model_dump(exclude_unset=True)


    for k,v in update_data.items():
        setattr(blog,k,v)

    db.add(blog)
    db.commit()
    redis_client.delete("blogs")

    redis_client.delete(
        f"blog:{blog.id}"
    )
    db.refresh(blog)

    return blog

def delete_blog(id:uuid.UUID,db:Session,user:UserModel):
    blog = db.get(BlogModel, id)

    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    if user.role != UserRole.ADMIN:
        if blog.user_id != user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed"
            )
    db.delete(blog)
    db.commit()
    redis_client.delete(
    f"blog:{blog.id}"
)
    return None
