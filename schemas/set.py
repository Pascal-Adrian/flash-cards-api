from pydantic import BaseModel, ConfigDict
from .category import Category
from .tag import Tag
from .card import CardCreate, CardUpdate, Card


class SetBase(BaseModel):
    title: str
    description: str
    level: int
    category: Category
    tags: list[Tag]


class SetCreate(SetBase):
    cards: list[CardCreate]


class Set(SetBase):
    id: int
    cards: list[Card]
    last_opened: str | None = None

    model_config = ConfigDict(from_attributes=True)


class SetUpdate(SetBase):
    cards: list[CardUpdate]
    last_opened: str | None = None

    model_config = ConfigDict(from_attributes=True)
