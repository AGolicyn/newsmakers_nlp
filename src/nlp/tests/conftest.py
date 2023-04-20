import os
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


TEST_SQLALCHEMY_DATABASE_URL = os.environ.get("ASYNC_TEST_DATABASE_URL")
engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True, future=True)
Base = declarative_base()

TestSessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def session():
    async with TestSessionFactory() as session:
        try:
            print("SESSION YIELDED")
            yield session
        finally:
            print("SESSION CLOSING")
            await session.execute(text("DELETE FROM news_title"))
            await session.execute(text("DELETE FROM cons_data"))
            await session.commit()
            await session.close()
            print("SESSION CLOSED")


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


titles = [
    {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/putin-soglasilsia-s-ideej-mincifry-vnedrit-ispolzovanie-qr-koda-vmesto-pasporta.html",
        "lang": "RU",
        "time": "2023-02-15 21:45:52.973532",
        "title": "Date test data",
        "country": "Russia",
    },
    {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/rossiia-sozyv94580305za-oon-po-diversiiam-na-severnyh-potokah.html?_openstat=rg.ru;blocks;maintoday-index;article",
        "lang": "RU",
        "time": "2023-02-16 21:45:52.974225",
        "title": 'Россия созывает 22 февраля заседание Совбеза ООН по диверсиям на "Северных потоках"',
        "country": "Russia",
    },
    {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/rossiia-sozyvaet-22-fevralia-zasedanie-sovbeza-oon-po-diversiiam-na-severnyh-potokah.html?_openstat=rg.ru;blocks;maintoday-index;article",
        "lang": "EN",
        "time": "2023-02-17 21:45:52.974225",
        "title": "Some title i dont care",
        "country": "Russia",
    },
    {
        "url": "https://rg.ru/",
        "href": "https://rg.ru/2023/02/15/rossiia-sozyvaet-22-fevralia3646sedanie-sovbeza-oon-po-diversiiam-na-severnyh-potokah.html?_openstat=rg.ru;blocks;maintoday-index;article",
        "lang": "EN",
        "time": "2023-02-17 21:45:52.974225",
        "title": "Another title i dont care",
        "country": "Britain",
    },
]
