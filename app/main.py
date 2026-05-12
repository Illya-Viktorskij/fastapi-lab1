from fastapi import FastAPI
from app.routers import users, categories, posts, comments, profiles

app = FastAPI(
    title="Users API",
    description="CRUD з реальною PostgreSQL БД",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(profiles.router)


@app.get("/")
def root():
    return {"message": "Hello World"}