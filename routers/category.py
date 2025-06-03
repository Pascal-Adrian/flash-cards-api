from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from cruds import category
from schemas import CategoryCreate, Category
from jwt_token import require_role_from_cookie


CategoryRouter = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@CategoryRouter.get("/", response_model=list[Category])
async def get_all_categories(db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("user"))):
    result = await category.get_all(db)
    return result


@CategoryRouter.get("/{id}", response_model=Category | None)
async def get_category(id: int, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await category.get(db, id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Category with id {id} not found.")

    return result


@CategoryRouter.post("/", response_model=Category)
async def create_category(category_create: CategoryCreate, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await category.create(db, category_create)

    return result


@CategoryRouter.put("/{id}", response_model=Category | None)
async def update_category(id: int, category_update: CategoryCreate, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await category.update(db, id, category_update)
    return result


@CategoryRouter.delete("/{id}", response_model=None)
async def delete_category(id: int, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await category.delete(db, id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Category with id {id} not found.")
