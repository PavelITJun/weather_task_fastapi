from sqlalchemy import Index
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON
from typing import Dict


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    IP: Mapped[str]
    history: Mapped[Dict] = mapped_column(JSON)
    last_query: Mapped[str]


class Cities(Base):
    __tablename__ = 'cities'

    city: Mapped[str] = mapped_column(primary_key=True)
    