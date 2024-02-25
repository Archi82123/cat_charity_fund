from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import AbstractBase


class Donation(AbstractBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Пожертвование "{self.comment}"'
        )
