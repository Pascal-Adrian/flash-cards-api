from sqlalchemy.orm import Session
from models import Tag
from schemas import TagCreate, Tag as TagSchema


async def get(db: Session, id: int) -> TagSchema | None:
    result = db.query(Tag).filter(Tag.id == id).first()  # type: ignore

    if result:
        return TagSchema(**result.__dict__)

    return None


async def get_all(db: Session) -> list[TagSchema]:
    results = db.query(Tag).all()  # type: ignore

    if results:
        return [TagSchema(**result.__dict__) for result in results]

    return []


async def create(db: Session, tag: TagCreate) -> TagSchema:
    new_tag = Tag(**tag.__dict__)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return TagSchema(**new_tag.__dict__)


async def update(db: Session, id: int, tag: TagCreate) -> TagSchema | None:
    existing_tag = db.query(Tag).filter(Tag.id == id).first()  # type: ignore

    if not existing_tag:
        return None

    for key, value in tag.__dict__.items():
        setattr(existing_tag, key, value)

    db.commit()
    db.refresh(existing_tag)

    return TagSchema(**existing_tag.__dict__)


async def delete(db: Session, id: int) -> bool:
    existing_tag = db.query(Tag).filter(Tag.id == id).first()  # type: ignore

    if not existing_tag:
        return False

    db.delete(existing_tag)
    db.commit()

    return True