import asyncio
import datetime
import time

from collections import defaultdict
from loguru import logger
from sqlalchemy.orm import Session
from uuid import UUID

from .word_cloud import build_wordcloud
from nlp.crud import title, cons
from .settings import SUPPORTED_COUNTRIES, language_manager
from concurrent.futures import ProcessPoolExecutor
from functools import partial


async def process_multi(db: Session):
    max_workers = len(SUPPORTED_COUNTRIES)
    start = time.time()
    result = {}
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        logger.debug(f'Start multiprocessing with {pool._max_workers} workers')
        loop = asyncio.get_running_loop()
        tasks = []

        for country in SUPPORTED_COUNTRIES:
            prc = Processor(country)
            data = prc.get_data(db=db)
            process_country = partial(prc.process_daily_data, data)
            tasks.append(loop.run_in_executor(pool, process_country))

        res = await asyncio.gather(*tasks)
        for r in res:
            result.update(r)
    Processor.insert_data(db=db, result=result)
    end = time.time() - start

    logger.debug(f'End multiprocessing, with {end}')

class Processor:
    def __init__(self, country: str, date: datetime.date = datetime.date.today()):
        self.date = date
        self.country, self.lang, self.nlp, self.ent, self.pipes \
            = language_manager(country=country)

    def get_data(self, db: Session):
        logger.debug('Getting data from db')
        return title.get_daily_titles_by_lang_and_country(db=db,
                                                          date=self.date,
                                                          lang=self.lang,
                                                          country=self.country)

    def process_daily_data(self, data: list):
        entities = self._entity_extractor(data)
        logger.debug('Calculating most common')
        common_entity_names = (
            self._accept_frequency(entity, frequency)
            for entity, frequency, date
            in self.entity_generator(entities, date=self.date)
        )
        common_entity_names = {k: v for k, v in common_entity_names}
        common_entities_with_id = self._common_entities_intersection(entities, common_entity_names)
        return {self.country: common_entities_with_id}

    def _common_entities_intersection(self, entities: dict[str, defaultdict[str, list[UUID]]],
                                      common_entity_names: dict[str, list[str]]) -> \
            dict[str, dict[str, list[UUID]]]:
        """Для самых распространенных сущностей получаем спсок uuid,
        в которых они упоминаются"""
        result = {}
        for entity in entities:
            temp = {}
            for entity_name in common_entity_names[entity]:
                if entity_name in entities[entity]:
                    temp[entity_name] = entities[entity][entity_name]
            result[self.ent[entity]] = temp
        return result

    def _accept_frequency(self, entity: str,
                          frequencies: dict):
        """Для каждой сущности и имени сущности считаем количество повторений,
         -> строим облако слов и выделяем 10 самых распространенных"""
        build_wordcloud(entity=entity,
                        frequencies=frequencies,
                        date=self.date,
                        country=self.country,
                        ent_mapper=self.ent)
        return self._most_common_entity_names(entity=entity, frequencies=frequencies)

    @staticmethod
    def _most_common_entity_names(entity: str, frequencies: dict):
        sorted_freq = sorted(frequencies, key=frequencies.get, reverse=True)
        return entity, sorted_freq[:10]

    def _entity_extractor(self, data: list):
        """Извлекаем список сущностей (по категориям) из текста и
        ассоциируем с каждой стрОки(id), в которых она упоминается"""
        logger.debug('Extracting entities')
        entities: dict[str, defaultdict[str, list[UUID]]] = \
            {ent: defaultdict() for ent in self.ent}
        for row in data:
            with self.nlp.select_pipes(enable=self.pipes):
                doc_ent = self.nlp(row.data['title'])
                for ent in doc_ent.ents:
                    if ent.label_ in self.ent:
                        entities[ent.label_].setdefault(ent.lemma_, []).append(str(row.id))
        return entities

    @staticmethod
    def entity_generator(entities: dict[str, defaultdict[str, list[UUID]]],
                         date: datetime.date = datetime.date.today()):
        for entity in entities:
            frequencies = {}
            for name in entities[entity]:
                frequencies[name] = len(entities[entity][name])
            yield entity, frequencies, date

    @staticmethod
    def insert_data(db: Session, result: dict):
        """Вставить данные базу данных"""
        cons.insert_daily_result(db=db, entities=result)
