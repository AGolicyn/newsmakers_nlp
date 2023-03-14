import datetime
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from nlp.db.session import ConsolidatedData
from sqlalchemy import insert, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Mapping


async def insert_daily_result(db: AsyncSession,
                              entities: Mapping,
                              date: datetime.date = datetime.date.today()):
    try:
        new_res = await db.execute(insert(ConsolidatedData)
                                   .values(entities=entities,
                                           date=date)
                                   .returning(ConsolidatedData))
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(repr(e))
    else:
        return new_res.scalar_one_or_none()


async def get_daily_results(db: AsyncSession, date: datetime.date, country: str):
    res = await db.execute(text(
        f"SELECT entities->> ('{country}') FROM cons_data "
        f"WHERE date(date) = date('{date}')"

    ))
    return res.scalar_one_or_none()
