from sqlalchemy.orm import Session
from models import Category
from schemas import CategoryCreate, Category as CategorySchema


async def get(db: Session, id: int) -> CategorySchema | None:
    result = db.query(Category).filter(Category.id == id).first()  # type: ignore

    if result:
        return CategorySchema(**result.__dict__)

    return None


async def get_all(db: Session) -> list[CategorySchema]:
    results = db.query(Category).all()  # type: ignore

    if results:
        return [CategorySchema(**result.__dict__) for result in results]

    return []


async def create(db: Session, category: CategoryCreate) -> CategorySchema:
    new_category = Category(**category.__dict__)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return CategorySchema(**new_category.__dict__)


async def update(db: Session, id: int, category: CategoryCreate) -> CategorySchema | None:
    existing_category = db.query(Category).filter(Category.id == id).first()  # type: ignore

    if not existing_category:
        return None

    for key, value in category.__dict__.items():
        setattr(existing_category, key, value)

    db.commit()
    db.refresh(existing_category)

    return CategorySchema(**existing_category.__dict__)


async def delete(db: Session, id: int) -> bool:
    existing_category = db.query(Category).filter(Category.id == id).first()  # type: ignore

    if not existing_category:
        return False

    db.delete(existing_category)
    db.commit()

    return True

