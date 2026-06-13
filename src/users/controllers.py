from sqlalchemy.orm import Session
from src.users.models import UserModel,UserRole
from src.users.schemas import UserSchema,LoginSchema
from fastapi import HTTPException,status
from pwdlib import PasswordHash
from datetime import datetime,timedelta
import jwt
from src.profiles.models import ProfileModel
from src.utils.settings import settings
from src.utils.redis import redis_client


password_hash = PasswordHash.recommended()
EXP_TIME = 30


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)

def register(body:UserSchema,db:Session):
    if body.role == UserRole.ADMIN:

        admin_exists = (
            db.query(UserModel)
            .filter(UserModel.role == UserRole.ADMIN)
            .first()
        )

        if admin_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin already exists"
            )
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already Exists"
        )
    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        email = body.email,
        hash_password=hash_password,
        role=body.role


        
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    profile = ProfileModel(
        bio="",
        user_id=new_user.id
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    
    return new_user


def login (body:LoginSchema,db:Session):
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found"
        )
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect password"
        )
    exp_time = datetime.now() + timedelta(minutes=EXP_TIME)

    token = jwt.encode(
    {
        "_id": str(user.id),
        "role": user.role.value,
        "exp": exp_time,
    },
    
    settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
)
    redis_client.set(
    f"session:{user.id}",
    token,
    ex=1800
)
        
    return { "access_token": token,
    "token_type": "bearer",
    "user": {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.created_at
    }
}



def logout(user: UserModel):

    redis_client.delete(
        f"session:{user.id}"
    )

    return {
        "message": "Logged out successfully"
    }