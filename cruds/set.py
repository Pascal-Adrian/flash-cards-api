from sqlalchemy.orm import Session
from models import Set, Card, SetTag, Category, Tag
from schemas import SetCreate, Set as SetSchema, SetUpdate


async def get(db: Session, id: int) -> SetSchema | None:
    result = db.query(Set).filter(Set.id == id).first()  # type: ignore

    if result:
        return SetSchema.from_orm(result)

    return None


async def get_all(db: Session, skip: int = 0, limit: int = 15) -> list[SetSchema]:
    results = db.query(Set).offset(skip).limit(limit).all()  # type: ignore

    if results:
        return [SetSchema.from_orm(result) for result in results]

    return []


async def create(db: Session, set_create: SetCreate) -> SetSchema:
    new_set = Set(
        title=set_create.title,
        description=set_create.description,
        level=set_create.level,
        category_id=set_create.category.id,
        last_opened=None
    )

    tag_ids = [tag.id for tag in set_create.tags]
    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

    new_set.tags = tags

    new_set.cards = [Card(question=card.question, answer=card.answer) for card in set_create.cards]

    db.add(new_set)
    db.commit()
    db.refresh(new_set)

    return SetSchema.from_orm(new_set)


async def update(db: Session, id: int, set_update: SetUpdate) -> SetSchema | None:
    existing_set = db.query(Set).filter(Set.id == id).first()  # type: ignore

    if not existing_set:
        return None

    existing_set.title = set_update.title
    existing_set.description = set_update.description
    existing_set.level = set_update.level
    existing_set.category_id = set_update.category.id
    existing_set.last_opened = None

    # Update tags
    tag_ids = [tag.id for tag in set_update.tags]
    existing_set.tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

    # Update cards
    existing_set_cards = existing_set.cards
    for card in existing_set_cards:
        if card.id in [c.id for c in set_update.cards]:
            card_update = next(c for c in set_update.cards if c.id == card.id)
            card.question = card_update.question
            card.answer = card_update.answer
        else:
            db.delete(card)

    for card in set_update.cards:
        if not card.id:
            new_card = Card(question=card.question, answer=card.answer)
            existing_set.cards.append(new_card)

    db.commit()
    db.refresh(existing_set)

    return SetSchema.from_orm(existing_set)


async def delete(db: Session, id: int) -> bool:
    existing_set = db.query(Set).filter(Set.id == id).first()  # type: ignore

    if not existing_set:
        return False

    db.delete(existing_set)
    db.commit()

    return True