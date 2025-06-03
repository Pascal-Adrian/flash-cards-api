from pydantic import BaseModel, ConfigDict


class CardBase(BaseModel):
    question: str
    answer: str


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CardUpdate(BaseModel):
    id: int | None = None
    question: str
    answer: str

    model_config = ConfigDict(from_attributes=True)