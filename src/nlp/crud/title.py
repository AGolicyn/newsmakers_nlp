import datetime
from loguru import logger
from sqlalchemy.orm import Session
from ..db.session import NewsTitle
from sqlalchemy import insert, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Mapping
from uuid import UUID


def insert_title(db: Session, title: Mapping):
    try:
        new_title = db.execute(insert(NewsTitle)
                               .values(data=title)
                               .returning(NewsTitle)
                               ).scalar_one_or_none()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(repr(e))
    else:
        return new_title


def get_daily_titles(db: Session, date: datetime.date = datetime.date.today()):
    titles = db.execute(text("SELECT *"
                             "FROM news_title "
                             f"WHERE date(data->>'time') = date('{date}')"))
    return titles


def get_daily_titles_by_lang_and_country(db: Session,
                                         lang: str, country: str,
                                         date: datetime.date = datetime.date.today(),
                                         ):
    titles = db.execute(text("SELECT *"
                             "FROM news_title "
                             f"WHERE date(data->>'time') = date('{date}')"
                             f"AND data->>'lang' = '{lang}'"
                             f"AND data->>'country' = '{country}'"
                             )).all()
    return titles


def get_title_by_id(db: Session, id: UUID):
    title = db.execute(text("SELECT data->>'title' "
                            "FROM news_title "
                            f"WHERE id = ('{id}')")).scalar_one()
    return title
