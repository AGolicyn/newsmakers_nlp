import datetime

from loguru import logger
from typing import Mapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, Date, func, desc
from sqlalchemy.exc import SQLAlchemyError

from nlp.db.session import NewsTitle


async def insert_title(db: AsyncSession, title: Mapping):
    try:
        stmt = insert(NewsTitle).values(data=title).returning(NewsTitle)
        nothing_to_do = stmt.on_conflict_do_nothing()
        new_title = await db.execute(nothing_to_do)
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(repr(e))
    else:
        return new_title.scalar_one_or_none()


async def get_daily_titles_by_lang_and_country(
    db: AsyncSession,
    lang: str,
    country: str,
    date: datetime.date = datetime.date.today(),
):
    titles = await db.execute(
        select(NewsTitle)
        .where(NewsTitle.data["time"].astext.cast(Date) == date)
        .where(NewsTitle.data["lang"].astext == lang)
        .where(NewsTitle.data["country"].astext == country)
    )
    result = titles.scalars().all()
    return result


async def get_day_url_frequency(
    db: AsyncSession, date: datetime.date = datetime.date.today()
):
    urls = await db.execute(
        select(
            NewsTitle.data["url"].astext.label("urls"),
            func.count(NewsTitle.data["url"].astext).label("frequency"),
        )
        .where(NewsTitle.data["time"].astext.cast(Date) == date)
        .group_by("urls")
        .order_by(desc("frequency"))
    )
    return urls.fetchall()
