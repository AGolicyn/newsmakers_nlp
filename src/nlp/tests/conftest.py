import pytest
from ..db.session import *
from ..crud.title import *
from .test_processing.data_garbage import *

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@db:5432/news_title"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db():
    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.execute(text('DELETE FROM news_title'))
        test_db.execute(text('DELETE FROM cons_data'))
        test_db.commit()
        test_db.close()


@pytest.fixture()
def fill_news_title_with_data(db: Session):
    title_1 = {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/putin-soglasilsia-s-ideej-mincifry-vnedrit-ispolzovanie-qr-koda-vmesto-pasporta.html",
        "lang": "RU", "time": "2023-02-15 21:45:52.973532",
        "title": "Date test data",
        "country": "Russia"
    }

    # Другая дата
    title_2 = {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/rossiia-sozyvaet-22-fevralia-zasedanie-sovbeza-oon-po-diversiiam-na-severnyh-potokah.html?_openstat=rg.ru;blocks;maintoday-index;article",
        "lang": "RU", "time": "2023-02-16 21:45:52.974225",
        "title": "Россия созывает 22 февраля заседание Совбеза ООН по диверсиям на \"Северных потоках\"",
        "country": "Russia"
    }
    # Другой язык
    title_3 = {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/rossiia-sozyvaet-22-fevralia-zasedanie-sovbeza-oon-po-diversiiam-na-severnyh-potokah.html?_openstat=rg.ru;blocks;maintoday-index;article",
        "lang": "EN", "time": "2023-02-17 21:45:52.974225",
        "title": "Some title i dont care",
        "country": "Russia"
    }
    # Другая страна
    title_4 = {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/rossiia-sozyvaet-22-fevralia-zasedanie-sovbeza-oon-po-diversiiam-na-severnyh-potokah.html?_openstat=rg.ru;blocks;maintoday-index;article",
        "lang": "EN", "time": "2023-02-17 21:45:52.974225",
        "title": "Another title i dont care",
        "country": "Britain"
    }

    insert_title(db=db, title=title_1)
    insert_title(db=db, title=title_2)
    insert_title(db=db, title=title_3)
    insert_title(db=db, title=title_4)

@pytest.fixture()
def get_prepared_en_data(db: Session):
    for title in ENGLISH_PREPARED_DATA:
        insert_title(db=db, title=title)
    day = datetime.date(2023, 2, 17)
    data = get_daily_titles_by_lang_and_country(db=db, lang='EN', country='USA', date=day)
    return data

@pytest.fixture()
def get_prepared_ru_data(db: Session):
    ids = []
    for title in RUSSIAN_PREPARED_DATA:
        ids.append(insert_title(db=db, title=title))
    day = datetime.date(2023, 2, 17)
    data = get_daily_titles_by_lang_and_country(db=db, lang='RU', country='Russia', date=day)
    return {"data": data, "ids": ids}
