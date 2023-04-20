import pytest
import datetime

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from nlp.db.session import NewsTitle

from nlp.processing.processing import Processor
from nlp.crud.title import insert_title, get_daily_titles_by_lang_and_country
from .data_garbage import (
    ENGLISH_PREPARED_DATA,
    GERMANY_PREPARED_DATA,
    RUSSIAN_PREPARED_DATA,
)


async def get_title_by_id(db: AsyncSession, id: UUID):
    title = await db.execute(select(NewsTitle.data["title"]).where(NewsTitle.id == id))
    return title.scalar_one()


@pytest.mark.asyncio
async def test_entity_extractor_for_en_language(session: AsyncSession):
    for title in ENGLISH_PREPARED_DATA:
        await insert_title(db=session, title=title)
    day = datetime.date(2023, 2, 17)
    data = await get_daily_titles_by_lang_and_country(
        db=session, lang="EN", country="USA", date=day
    )

    proc = Processor(country="USA")
    result = proc._entity_extractor(data)

    for entity in ("GPE", "ORG", "PERSON"):
        assert bool(result[entity])
    for country in ("russia", "england", "usa"):
        assert country in "".join(result["GPE"]).lower()
    for person in ("elton", "kennedy"):
        assert person in "".join(result["PERSON"]).lower()
    assert "burger king" in "".join(result["ORG"]).lower()
    id = result["PERSON"]["kennedy"][0]

    title = await get_title_by_id(db=session, id=id)
    assert title == ENGLISH_PREPARED_DATA[2]["title"]


@pytest.mark.asyncio
async def test_entity_extractor_for_ru_language(session: AsyncSession):
    for title in RUSSIAN_PREPARED_DATA:
        await insert_title(db=session, title=title)
    day = datetime.date(2023, 2, 17)
    data = await get_daily_titles_by_lang_and_country(
        db=session, lang="RU", country="Russia", date=day
    )

    proc = Processor(country="Russia")
    result = proc._entity_extractor(data)

    # Проверяем все ли категории сущностей были найдены
    for entity in ("LOC", "ORG", "PER"):
        assert bool(result[entity])
    # Проверяем, что по каждой категории все наименования найдены
    for country in ("россия", "германия"):
        assert country in "".join(result["LOC"]).lower()
    for person in ("сталин", "путин"):
        assert person in "".join(result["PER"]).lower()
    assert "мвд" in "".join(result["ORG"]).lower()
    # Проверяем, что сохраненные id, действительно указывают на нужные строки базы
    id = result["LOC"]["россия"][0]
    title = await get_title_by_id(db=session, id=id)
    assert title == RUSSIAN_PREPARED_DATA[0]["title"]


@pytest.mark.asyncio
async def test_entity_extractor_for_de_language(session: AsyncSession):
    for title in GERMANY_PREPARED_DATA:
        await insert_title(db=session, title=title)
    day = datetime.date(2023, 2, 21)
    data = await get_daily_titles_by_lang_and_country(
        db=session, lang="DE", country="Germany", date=day
    )

    proc = Processor(country="Germany")
    result = proc._entity_extractor(data)
    # Проверяем все ли категории сущностей были найдены
    for entity in ("LOC", "ORG", "PER"):
        assert bool(result[entity])

    # Проверяем, что по каждой категории все наименования найдены
    for person in ("toto wolf", "angela merkel", "robert lewandowski"):
        assert person in "".join(result["PER"]).lower()

    for location in ("berlin", "brandenburger tor"):
        assert location in "".join(result["LOC"]).lower()

    for organization in ("bayern münchen", "mercedes amg"):
        assert organization in "".join(result["ORG"]).lower()

    # Проверяем, что сохраненные id, действительно указывают на нужные строки базы
    id = result["PER"]["Robert Lewandowski"][0]
    title = await get_title_by_id(db=session, id=id)

    assert title == GERMANY_PREPARED_DATA[0]["title"]


#
# @pytest.mark.skipif(reason='Dont understand why am i trying to test this, and what im actually testing:)')
# def test_entity_generator():
#     entities = {
#         'LOC':
#             defaultdict(None, {
#                 'россия': ['791e8eff-6d46-4a07-871b-7b3b1fc2f01f', 'e11de3e3-6cc7-4ff4-9773-0212c9fbac19'],
#                 'германия': ['0d02a2b2-ab22-44ec-8728-5d07bf444dd3'],
#                 'кремль': ['0d02a2b2-ab22-44ec-8728-5d07bf444dd3']}),
#         'PER': defaultdict(None, {
#             'Сталин': ['791e8eff-6d46-4a07-871b-7b3b1fc2f01f', 'e11de3e3-6cc7-4ff4-9773-0212c9fbac19'],
#             'Путин': ['0d02a2b2-ab22-44ec-8728-5d07bf444dd3']}),
#         'ORG': defaultdict(None, {
#             'мвд': ['791e8eff-6d46-4a07-871b-7b3b1fc2f01f', 'e11de3e3-6cc7-4ff4-9773-0212c9fbac19']})
#     }
#     result = {}
#     for entity, freq, _ in Processor.entity_generator(entities=entities, date=datetime.date(2023, 2, 17)):
#         result.update((entity, freq))
#     print(result)
