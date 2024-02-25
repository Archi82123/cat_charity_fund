from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationResponse(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationResponse):
    user_id: int
    invested_amount: int
    fully_invested: int
    close_date: Optional[datetime]
