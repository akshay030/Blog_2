import time

from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.logger import logger
from src.admin.controllers import create_api_log
from src.utils.db import LocalSession


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start_time = time.time()

        response = await call_next(request)

        user_id = getattr(
            request.state,
            "user_id",
            None
        )

        process_time = round(
            time.time() - start_time,
            3
        )

        logger.info(
            f"IP={request.client.host} | "
            f"USER={user_id or 'ANONYMOUS'} | "
            f"{request.method} | "
            f"{request.url.path} | "
            f"{response.status_code} | "
            f"{process_time}s"
        )

        session = LocalSession()

        try:
            create_api_log(
                db=session,
                user_id=user_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                response_time=process_time
            )
        finally:
            session.close()

        return response