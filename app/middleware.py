import time
import threading
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# Configuration
RATE_LIMIT = 100  # max requests
WINDOW_SECONDS = 3600  # per IP, in seconds

# In-memory storage for rate-limiting
request_log = {}
lock = threading.Lock()

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        with lock:
            log = request_log.setdefault(client_ip, [])
            # Remove old timestamps outside the window
            request_log[client_ip] = [t for t in log if t > current_time - WINDOW_SECONDS]

            if len(request_log[client_ip]) >= RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={
                        "status": 429,
                        "message": "Rate limit exceeded. Try again later."
                    }
                )

            # Allow this request
            request_log[client_ip].append(current_time)

        response = await call_next(request)
        return response
