from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.utils.helper import is_authenticated
from src.blogs.schemas import BlogResponseSchema,BlogSchema,UpdateBlogSchema
from src.users.models import UserModel
from src.blogs import controllers
from fastapi import status
from typing import List
import uuid
from src.utils.permissions import require_roles
from src.users.models import UserRole

blog_routes = APIRouter(prefix='/blogs',tags=["Blogs"])

@blog_routes.get('/',response_model=List[BlogResponseSchema],status_code=status.HTTP_200_OK)
def get_all_blogs(db:Session = Depends(get_db)):
    return controllers.get_all_blogs(db)

@blog_routes.get('/{id}',response_model=BlogResponseSchema,status_code=status.HTTP_200_OK)
def get_blogs_by_id(id:uuid.UUID,db:Session = Depends(get_db)):
    return controllers.get_blog_by_id(id,db)

@blog_routes.post('/',response_model=BlogResponseSchema,status_code=status.HTTP_201_CREATED)
def create_blog(body:BlogSchema,db:Session=Depends(get_db),user:UserModel = Depends( require_roles(
            UserRole.AUTHOR,
            UserRole.ADMIN
        ))):
    return controllers.create_blog(body,db,user)

@blog_routes.put('/{id}',response_model=BlogResponseSchema,status_code=status.HTTP_201_CREATED)
def update_blog(id:uuid.UUID,body:UpdateBlogSchema,db:Session=Depends(get_db),user :UserModel= Depends( require_roles(
            UserRole.AUTHOR,
            UserRole.ADMIN
        ))):
    return controllers.update_blog(id,body,db,user)


@blog_routes.delete('/blog/{id}',response_model=None,status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:uuid.UUID,db:Session=Depends(get_db),user:UserModel= Depends( require_roles(
            UserRole.AUTHOR,
            UserRole.ADMIN
        ))):
    return controllers.delete_blog(id,db,user)