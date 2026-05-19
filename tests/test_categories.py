from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.category import create_category, get_category, get_categories, delete_category


async def test_crud_create_category(db: AsyncSession):
    cat = await create_category(db, "TestCat", "desc")
    assert cat.id is not None
    assert cat.name == "TestCat"


async def test_crud_get_category(db: AsyncSession):
    cat = await create_category(db, "GetCat", "desc")
    fetched = await get_category(db, cat.id)
    assert fetched is not None


async def test_crud_get_categories(db: AsyncSession):
    cats = await get_categories(db)
    assert isinstance(cats, list)


async def test_crud_delete_category(db: AsyncSession):
    cat = await create_category(db, "DelCat", "desc")
    deleted = await delete_category(db, cat.id)
    assert deleted is not None


async def test_api_get_categories(client: AsyncClient):
    response = await client.get("/categories/")
    assert response.status_code == 200


async def test_api_create_category(client: AsyncClient):
    response = await client.post("/categories/", json={
        "name": "APICat",
        "description": "API test category"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "APICat"


async def test_api_get_category_not_found(client: AsyncClient):
    response = await client.get("/categories/99999")
    assert response.status_code == 404


async def test_api_delete_category(client: AsyncClient):
    create = await client.post("/categories/", json={
        "name": "ToDeleteCat",
        "description": "delete me"
    })
    cat_id = create.json()["id"]
    response = await client.delete(f"/categories/{cat_id}")
    assert response.status_code == 200