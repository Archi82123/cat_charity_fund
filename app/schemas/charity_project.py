from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.core.constants import MAX_NAME_LENGTH, MIN_AMOUNT, MIN_NAME_LENGTH


class CharityProjectBase(BaseModel):
    name: str
    description: str
    full_amount: int

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(...,
                      min_length=MIN_NAME_LENGTH,
                      max_length=MAX_NAME_LENGTH
                      )
    description: str = Field(...,
                             min_length=MIN_NAME_LENGTH,
                             max_length=MAX_NAME_LENGTH
                             )
    full_amount: int = Field(..., ge=MIN_AMOUNT)


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None,
                                min_length=MIN_NAME_LENGTH,
                                max_length=MAX_NAME_LENGTH
                                )
    description: Optional[str] = Field(None,
                                       min_length=MIN_NAME_LENGTH,
                                       max_length=MAX_NAME_LENGTH
                                       )
    full_amount: Optional[int] = Field(None, ge=MIN_AMOUNT)


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: int
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
