from fastapi import FastAPI
from routers import users

app = FastAPI(
    title="Users API",
    description="CRUD для юзерів з емуляцією БД",
    version="1.0.0"
)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World"}