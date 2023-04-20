import uuid
import datetime
import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import func, UUID, text, Index
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from collections.abc import Mapping
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import Date

LOCAL_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/news_title"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", default=LOCAL_DATABASE_URL)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
Base = declarative_base()

AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session


class NewsTitle(Base):
    __tablename__ = "news_title"
    __table_args__ = (Index("unique_href", text("(data->>'href')"), unique=True),)

    id: Mapped[uuid] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    data: Mapped[Mapping] = mapped_column(JSONB)


class ConsolidatedData(Base):
    __tablename__ = "cons_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    entities: Mapped[Mapping] = mapped_column(JSONB)
    date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())
