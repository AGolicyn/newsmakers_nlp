import datetime
import uuid
import os

from sqlalchemy import create_engine, text, func
from sqlalchemy.types import Date, UUID
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from collections.abc import Mapping
from sqlalchemy.dialects.postgresql import JSONB


LOCAL_DATABASE_URL = 'postgresql://postgres:postgres@db:5432/news_title'
SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', default=LOCAL_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase): pass

Base.metadata.create_all(bind=engine)

class NewsTitle(Base):
    __tablename__ = 'news_title'

    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True),
                                     primary_key=True,
                                     server_default=text('gen_random_uuid()'))
    data: Mapped[Mapping] = mapped_column(JSONB)


class ConsolidatedData(Base):
    __tablename__ = 'cons_data'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    entities: Mapped[Mapping] = mapped_column(JSONB)
    date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())
