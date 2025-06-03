from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from cruds import set
from schemas import SetCreate, Set, SetUpdate
from jwt_token import require_role_from_cookie


SetRouter = APIRouter(
    prefix="/sets",
    tags=["sets"]
)


@SetRouter.get("/", response_model=list[Set])
async def get_all_sets(db=Depends(get_db), skip: int = 0, limit: int = 15, payload: dict = Depends(require_role_from_cookie("user"))):
    result = await set.get_all(db, skip, limit)
    return result


@SetRouter.get("/{id}", response_model=Set | None)
async def get_set(id: int, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("user"))):
    result = await set.get(db, id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Set with id {id} not found.")

    return result


@SetRouter.post("/", response_model=Set)
async def create_set(set_create: SetCreate, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("user"))):
    result = await set.create(db, set_create)

    return result


@SetRouter.put("/{id}", response_model=Set | None)
async def update_set(id: int, set_update: SetUpdate, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("user"))):
    result = await set.update(db, id, set_update)

    if not result:
        raise HTTPException(status_code=404, detail=f"Set with id {id} not found.")

    return result


@SetRouter.delete("/{id}", response_model=None)
async def delete_set(id: int, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await set.delete(db, id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Set with id {id} not found.")

    return
