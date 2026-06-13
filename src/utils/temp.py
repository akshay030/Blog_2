from fastapi import APIRouter,Depends
from src.users.models import UserModel
from src.utils.helper import is_authenticated
from src.utils.redis import redis_client

test_routes = APIRouter(prefix="/test",tags=["test"])


@test_routes.get("/redis")
def redis_test():

    redis_client.set(
        "hello",
        "world"
    )

    value = redis_client.get("hello")

    return {
        "redis_value": value
    }
    
@test_routes.get("/redis-session")
def redis_session(
    user: UserModel = Depends(is_authenticated)
):
    return {
        "session": redis_client.ttl(
            f"session:{user.id}"
        )
    }