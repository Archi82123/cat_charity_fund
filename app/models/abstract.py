import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class AbstractBase(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(
        DateTime(timezone=True),
        default=datetime.datetime.utcnow
    )
    close_date = Column(DateTime(timezone=True))
