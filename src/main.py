from fastapi import FastAPI
from src.utils.db import Base,engine
from src.users.routes import user_routes
from src.users.models import UserModel
from src.blogs.routes import blog_routes
from src.blogs.models import BlogModel
from src.comments.models import CommentModel
from src.comments.routes import comments_routes
from src.profiles.models import ProfileModel
from src.profiles.routes import profile_routes
from src.llm.routes import ai_routes
from src.utils.temp import test_routes
from src.middleware.logging import LoggingMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.utils.limiter import limiter


app= FastAPI()
app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(LoggingMiddleware)
app.include_router(user_routes)
app.include_router(blog_routes)
app.include_router(comments_routes)
app.include_router(profile_routes)
app.include_router(ai_routes)
app.include_router(test_routes)

@app.get("/")
def health():
    return {
       "status": "Healthy"
    }