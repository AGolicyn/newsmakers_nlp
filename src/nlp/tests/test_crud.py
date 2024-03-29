import datetime

from uuid import UUID
from nlp.tests.conftest import titles
import pytest
from nlp.crud import title, cons
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from nlp.db.session import NewsTitle


async def get_titles(db: AsyncSession):
    ttls = await db.execute(select(NewsTitle))
    return ttls.all()


@pytest.mark.asyncio
async def test_insert_processed_data(session: AsyncSession):
    day_result = {
        "Russia": {
            "LOC": {
                "рф": [
                    "6fdc9ad0-5fc4-4037-b4a7-0d1fd1a5efef",
                    "3c9c4d17-65ba-44be-9b33-4c24f3d20048",
                ],
                "сша": [
                    "a13c9dc0-7628-4bf6-bf8c-fb968e440826",
                    "2b7a8a3e-808d-4326-9215-aa7026edea19",
                ],
            },
            "ORG": {
                "цб": [
                    "fff5b484-262e-4c9f-bf93-e957e898aded",
                    "4805e20c-6908-43d5-ae6a-49bf219b0a1d",
                ],
                "всу": ["827b7625-1110-4e51-9c43-c26b09a23dbc"],
            },
            "PER": {
                "Херш": [
                    "b61eb586-eed7-47e6-ac50-e8e1b1177e3b",
                    "8aa5d169-4944-466d-ab51-f22f55bcf002",
                ],
                "Путин": ["b04f697c-a7a0-48c4-ab79-6a92a308758e"],
            },
        }
    }
    today = datetime.date.today()
    inserted_data = await cons.insert_daily_result(db=session, entities=day_result)

    assert inserted_data.date == today
    assert "Russia" in inserted_data.entities
    assert "LOC" in inserted_data.entities["Russia"]
    assert "ORG" in inserted_data.entities["Russia"]
    assert "PER" in inserted_data.entities["Russia"]


@pytest.mark.asyncio
async def test_insert_title_data(session: AsyncSession):
    test_title = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.usatoday.com/moremoremoremoerelike_real_url",
        "lang": "EN",
        "time": "2023-02-15 21:45:55.270582",
        "title": "Tesla’s supercharger network to open to competing…",
        "country": "USA",
    }

    inserted_data = await title.insert_title(db=session, title=test_title)

    assert isinstance(inserted_data.id, UUID)
    assert inserted_data.data["url"] == test_title["url"]
    assert inserted_data.data["href"] == test_title["href"]
    assert inserted_data.data["lang"] == test_title["lang"]
    assert inserted_data.data["title"] == test_title["title"]
    assert inserted_data.data["time"] == test_title["time"]
    assert inserted_data.data["country"] == test_title["country"]


@pytest.mark.asyncio
async def test_insert_unique_href_one_day(session: AsyncSession):
    test_title = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test.com/",
        "lang": "EN",
        "time": "2023-02-15 21:45:55.270582",
        "title": "ONE title",
        "country": "USA",
    }

    same_href_but_later = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test.com/",
        "lang": "EN",
        "time": "2023-02-15 22:45:55.270582",
        "title": "ANOTHER title",
        "country": "USA",
    }

    await title.insert_title(db=session, title=test_title)
    await title.insert_title(db=session, title=same_href_but_later)

    result = await get_titles(db=session)

    assert len(result) == 1


@pytest.mark.asyncio
async def test_insert_unique_href_data_different_days(session: AsyncSession):
    test_title = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test.com/",
        "lang": "EN",
        "time": "2023-02-15 21:45:55.270582",
        "title": "ONE title",
        "country": "USA",
    }

    same_href_but_later = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test.com/",
        "lang": "EN",
        "time": "2023-02-16 22:45:55.270582",
        "title": "ANOTHER title",
        "country": "USA",
    }

    await title.insert_title(db=session, title=test_title)
    await title.insert_title(db=session, title=same_href_but_later)

    result = await get_titles(db=session)

    assert len(result) == 2


@pytest.mark.asyncio
async def test_insert_unique_title_different_days(session: AsyncSession):
    test_title = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test.com/",
        "lang": "EN",
        "time": "2023-02-15 21:45:55.270582",
        "title": "ONE title",
        "country": "USA",
    }

    same_title_but_later = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test2.com/",
        "lang": "EN",
        "time": "2023-02-16 22:56:55.270582",
        "title": "ONE title",
        "country": "USA",
    }

    await title.insert_title(db=session, title=test_title)
    await title.insert_title(db=session, title=same_title_but_later)

    result = await get_titles(db=session)

    assert len(result) == 2


@pytest.mark.asyncio
async def test_insert_unique_title_one_day(session: AsyncSession):
    test_title = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test.com/",
        "lang": "EN",
        "time": "2023-02-15 21:45:55.270582",
        "title": "ONE title",
        "country": "USA",
    }
    same_title_but_later = {
        "url": "https://www.usatoday.com/",
        "href": "https://www.test2.com/",
        "lang": "EN",
        "time": "2023-02-15 22:56:55.270582",
        "title": "ONE title",
        "country": "USA",
    }
    await title.insert_title(db=session, title=test_title)
    await title.insert_title(db=session, title=same_title_but_later)

    result = await get_titles(db=session)

    assert len(result) == 1


@pytest.mark.asyncio
async def test_gets_only_today_data(session: AsyncSession):
    for db_title in titles:
        await title.insert_title(db=session, title=db_title)
    date = datetime.date(2023, 2, 15)

    result = await title.get_daily_titles_by_lang_and_country(
        db=session, lang="RU", country="Russia", date=date
    )
    print(result)

    assert len(result) == 1
    assert result[0].data["title"] == "Date test data"
    assert str(date) in result[0].data["time"]


@pytest.mark.asyncio
async def test_gets_only_lang_and_country_needed(session: AsyncSession):
    for db_title in titles:
        await title.insert_title(db=session, title=db_title)
    date = datetime.date(2023, 2, 17)

    result = await title.get_daily_titles_by_lang_and_country(
        db=session, lang="EN", country="Britain", date=date
    )

    assert len(result) == 1
    assert result[0].data["title"] == "Another title i dont care"
    assert str(date) in result[0].data["time"]
