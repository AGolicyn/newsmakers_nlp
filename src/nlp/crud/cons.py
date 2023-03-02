import datetime
from loguru import logger
from sqlalchemy.orm import Session
from nlp.db.session import ConsolidatedData
from sqlalchemy import insert, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Mapping


def insert_daily_result(db: Session, entities: Mapping):
    try:
        new_res = db.execute(insert(ConsolidatedData)
                             .values(entities=entities)
                             .returning(ConsolidatedData)
                             ).scalar_one_or_none()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(repr(e))
    else:
        return new_res


def get_daily_results(db: Session, date: datetime.date, country: str):
    res = db.execute(text(
        f"SELECT entities->> ('{country}') FROM cons_data "
        f"WHERE date(date) = date('{date}')"

    )).scalar_one_or_none()
    return res
