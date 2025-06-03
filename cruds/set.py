from sqlalchemy.orm import Session
from models import Set
from schemas import SetCreate, Set as SetSchema


async def get(db: Session, id: int) -> SetSchema | None:
    result = db.query(Set).filter(Set.id == id).first()  # type: ignore

    if result:
        return SetSchema(**result.__dict__)

    return None


async def get_all(db: Session) -> list[SetSchema]:
    results = db.query(Set).all()  # type: ignore

    if results:
        return [SetSchema(**result.__dict__) for result in results]

    return []


async def create(db: Session, set_create: SetCreate) -> SetSchema:
    new_set = Set(**set_create.__dict__)
    db.add(new_set)
    db.commit()
    db.refresh(new_set)

    return SetSchema(**new_set.__dict__)


async def update(db: Session, id: int, set_update: SetCreate) -> SetSchema | None:
    existing_set = db.query(Set).filter(Set.id == id).first()  # type: ignore

    if not existing_set:
        return None

    for key, value in set_update.__dict__.items():
        setattr(existing_set, key, value)

    db.commit()
    db.refresh(existing_set)

    return SetSchema(**existing_set.__dict__)


async def delete(db: Session, id: int) -> bool:
    existing_set = db.query(Set).filter(Set.id == id).first()  # type: ignore

    if not existing_set:
        return False

    db.delete(existing_set)
    db.commit()

    return True