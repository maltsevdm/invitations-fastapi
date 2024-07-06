from enum import Enum
from pydantic import BaseModel, Field


class Sex(Enum):
    male = "male"
    female = "female"


class AnketaSchema(BaseModel):
    id: str
    accept: bool
    drinks: list[str] | None = None
    children: bool | None = None
    comment: str = ""


class Guest(BaseModel):
    names: list[str] = Field(min_length=1)
    sex: Sex | None = None
    has_children: bool = False


class GuestUpdate(BaseModel):
    names: list[str] | None = None
    sex: Sex | None = None
    has_children: bool | None = None
