from sqlalchemy import Column, String, Text

from app.core.db import PreBaseDonationCharity


class CharityProject(PreBaseDonationCharity):
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f'Фонд {self.name}'
