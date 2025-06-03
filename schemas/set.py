from pydantic import BaseModel
from .category import Category
from .tag import Tag
from .card import Card, CardCreate


class SetBase(BaseModel):
    title: str
    description: str
    level: int
    last_opened: str | None = None
    category: Category
    tags: list[Tag]


class SetCreate(SetBase):
    cards: list[CardCreate]


class Set(SetBase):
    id: int
    cards: list[Card]
