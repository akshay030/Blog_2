from src.profiles.schemas import UpdateProfileSchema
from src.profiles.models import ProfileModel
from src.users.models import UserModel
from src.utils.redis import redis_client
from sqlalchemy.orm import Session
from fastapi import HTTPException
import json


def edit_profile(
    body: UpdateProfileSchema,
    db: Session,
    user: UserModel
):
    profile = (
        db.query(ProfileModel)
        .filter(ProfileModel.user_id == user.id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    update_data = body.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(profile, key, value)

    db.commit()
    redis_client.delete(
    f"profile:{user.id}"
)
    db.refresh(profile)

    return profile

def get_my_profile(
    db: Session,
    user: UserModel
):

    cache_key = f"profile:{user.id}"

    cached_profile = redis_client.get(
        cache_key
    )

    if cached_profile:

        print("PROFILE CACHE HIT")

        return json.loads(cached_profile)

    print("PROFILE CACHE MISS")

    profile = (
        db.query(ProfileModel)
        .filter(
            ProfileModel.user_id == user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    profile_data = {
        "id": str(profile.id),
        "bio": profile.bio,

        "user_id": str(profile.user_id),

        "created_at": profile.created_at.isoformat(),
        "updated_at": profile.updated_at.isoformat()
    }

    redis_client.set(
        cache_key,
        json.dumps(profile_data),
        ex=300
    )

    return profile_data