from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import users, categories, posts, comments, profiles, auth

app = FastAPI(
    title="Users API",
    description="CRUD з JWT аутентифікацією",
    version="2.0.0"
)

# Автоматичні метрики FastAPI
Instrumentator().instrument(app).expose(app)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(profiles.router)


@app.get("/")
def root():
    return {"message": "Hello World"}