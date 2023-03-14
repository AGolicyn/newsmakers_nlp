import datetime
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from nlp.db.session import NewsTitle
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Mapping
from uuid import UUID


async def insert_title(db: AsyncSession, title: Mapping):
    try:
        stmt = insert(NewsTitle).values(data=title).returning(NewsTitle)
        nothing_to_do = stmt.on_conflict_do_nothing(
            index_elements=[text("(data->>'href')")]
        )
        new_title = await db.execute(nothing_to_do)
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(repr(e))
    else:
        return new_title.scalar_one_or_none()


async def get_daily_titles(db: AsyncSession, date: datetime.date = datetime.date.today()):
    titles = await db.execute(text("SELECT * "
                                   "FROM news_title "
                                   f"WHERE date(data->>'time') = date('{date}')"))
    return titles.all()


async def get_daily_titles_by_lang_and_country(db: AsyncSession,
                                               lang: str, country: str,
                                               date: datetime.date = datetime.date.today(),
                                               ):
    titles = await db.execute(text("SELECT * "
                                   "FROM news_title "
                                   f"WHERE date(data->>'time') = date('{date}')"
                                   f"AND data->>'lang' = '{lang}'"
                                   f"AND data->>'country' = '{country}'"
                                   ))
    result = titles.all()
    return result


async def get_title_by_id(db: AsyncSession, id: UUID):
    title = await db.execute(text("SELECT data->>'title' "
                                  "FROM news_title "
                                  f"WHERE id = ('{id}')"))
    return title.scalar_one()


async def get_day_url_frequency(db: AsyncSession, date: datetime.date = datetime.date.today()):
    urls = await db.execute(text(
        "SELECT data->>'url' as URL, count(*) as Frequency "
        "FROM news_title "
        f"WHERE date(data->>'time') = date('{date}')"
        "GROUP BY data->>'url'"
        "ORDER BY Frequency DESC"
    ))
    return urls.fetchall()
