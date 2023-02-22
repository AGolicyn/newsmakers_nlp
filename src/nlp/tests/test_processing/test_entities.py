import pytest

from ...processing.processing import *
from ...crud.title import *
from .data_garbage import *

def test_entity_extractor_for_en_language(db: Session, get_prepared_en_data):
    proc = Processor(country='USA')

    result = proc._entity_extractor(get_prepared_en_data)

    for entity in ('GPE', 'ORG', 'PERSON'):
        assert entity in result

    for country in ('russia', 'england', 'usa'):
        assert country in result['GPE']

    for person in ('elton john', 'kennedy'):
        assert person in result['PERSON']

    assert 'burger king' in result['ORG']

    id = result['PERSON']['kennedy'][0]

    title = get_title_by_id(db=db, id=id)

    assert title == ENGLISH_PREPARED_DATA[2]['title']

def test_entity_extractor_for_ru_language(db: Session, get_prepared_ru_data):
    proc = Processor(country='Russia')

    result = proc._entity_extractor(get_prepared_ru_data['data'])

    # Проверяем все ли категории сущностей были найдены
    for entity in ('LOC', 'ORG', 'PER'):
        assert entity in result
    # Проверяем, что по каждой категории все наименования найдены
    for country in ('россия', 'Германия'):
        assert country in result['LOC']

    for person in ('Сталин', 'Путин'):
        assert person in result['PER']

    assert 'мвд' in result['ORG']

    # Проверяем, что сохраненные id, действительно указывают на нужные строки базы
    id = result['LOC']['россия'][0]
    title = get_title_by_id(db=db, id=id)

    assert title == RUSSIAN_PREPARED_DATA[0]['title']
@pytest.mark.skip()
def test_entity_generator():
    entities = {'LOC':
                    defaultdict(None, {
                        'россия': ['791e8eff-6d46-4a07-871b-7b3b1fc2f01f', 'e11de3e3-6cc7-4ff4-9773-0212c9fbac19'],
                        'Германия': ['0d02a2b2-ab22-44ec-8728-5d07bf444dd3'],
                        'кремль': ['0d02a2b2-ab22-44ec-8728-5d07bf444dd3']}),
                'PER': defaultdict(None, {
                    'Сталин': ['791e8eff-6d46-4a07-871b-7b3b1fc2f01f', 'e11de3e3-6cc7-4ff4-9773-0212c9fbac19'],
                    'Путин': ['0d02a2b2-ab22-44ec-8728-5d07bf444dd3']}),
                'ORG': defaultdict(None, {
                    'мвд': ['791e8eff-6d46-4a07-871b-7b3b1fc2f01f', 'e11de3e3-6cc7-4ff4-9773-0212c9fbac19']})
                }
    result = {}
    ent = {}
    for entity, freq, _ in Processor.entity_generator(entities=entities, date=datetime.date(2023,2,17)):
        result.update((entity, freq))
    print(result)

