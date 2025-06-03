from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from cruds import tag
from schemas import TagCreate, Tag
from jwt_token import require_role_from_cookie


TagRouter = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


@TagRouter.get("/", response_model=list[Tag], dependencies=[Depends(require_role_from_cookie("user"))])
async def get_all_tags(db=Depends(get_db)):
    result = await tag.get_all(db)
    return result


@TagRouter.get("/{id}", response_model=Tag | None)
async def get_tag(id: int, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await tag.get(db, id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Tag with id {id} not found.")

    return result


@TagRouter.post("/", response_model=Tag)
async def create_tag(tag_create: TagCreate, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await tag.create(db, tag_create)

    return result


@TagRouter.put("/{id}", response_model=Tag | None)
async def update_tag(id: int, tag_update: TagCreate, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await tag.update(db, id, tag_update)
    return result


@TagRouter.delete("/{id}", response_model=None)
async def delete_tag(id: int, db=Depends(get_db), payload: dict = Depends(require_role_from_cookie("admin"))):
    result = await tag.delete(db, id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Tag with id {id} not found.")