import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import users, categories, posts, comments, profiles, auth
from app.metrics import HTTP_REQUEST_DURATION, ERRORS_TOTAL

app = FastAPI(
    title="Users API",
    description="CRUD з JWT аутентифікацією",
    version="2.0.0"
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)
instrumentator.instrument(app).expose(app, include_in_schema=False)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = None
    try:
        response = await call_next(request)
    except Exception as exc:
        ERRORS_TOTAL.labels(
            error_type=type(exc).__name__,
            endpoint=request.url.path
        ).inc()
        raise
    finally:
        if response is not None:
            duration = time.time() - start_time
            # Використовуємо route path якщо є, інакше url path
            route = request.url.path
            if hasattr(request, "scope") and "route" in request.scope:
                route_obj = request.scope.get("route")
                if route_obj and hasattr(route_obj, "path"):
                    route = route_obj.path
            HTTP_REQUEST_DURATION.labels(
                method=request.method,
                endpoint=route,
                status_code=response.status_code
            ).observe(duration)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    ERRORS_TOTAL.labels(
        error_type=type(exc).__name__,
        endpoint=request.url.path
    ).inc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(profiles.router)


@app.get("/")
def root():
    return {"message": "Hello World"}