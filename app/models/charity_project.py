from sqlalchemy import Column, String, Text

from app.core.constants import MAX_NAME_LENGTH
from app.models.abstract import AbstractBase


class CharityProject(AbstractBase):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Проект - "{self.name}"'
        )
