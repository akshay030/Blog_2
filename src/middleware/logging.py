import time

from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        user_id = getattr(request.state, "user_id", None)

        start_time = time.time()

        try:
            response = await call_next(request)

            process_time = round(
                time.time() - start_time,
                3
            )

            logger.info(
                f"IP={request.client.host} | "
                f"USER={user_id} | "
                f"{request.method} | "
                f"{request.url.path} | "
                f"{response.status_code} | "
                f"{process_time}s"
            )

            return response

        except Exception as e:

            logger.error(
                f"IP={request.client.host} | "
                f"USER={user_id} | "
                f"{request.method} | "
                f"{request.url.path} | "
                f"ERROR={str(e)}"
            )

            raise