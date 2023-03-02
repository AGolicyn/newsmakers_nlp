import datetime

from collections import defaultdict
from loguru import logger
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.orm import Session
from uuid import UUID

from .word_cloud import build_wordcloud
from nlp.crud import title, cons
from .settings import SUPPORTED_COUNTRIES, language_manager, ENT


def process(db: Session):
    result = {}
    for country in SUPPORTED_COUNTRIES:
        logger.debug(f'Start processing {country}...')
        prc = Processor(country)
        res = prc.process_daily_data(db=db)
        result.update(res)
        logger.debug(f'{country} processed')
    logger.debug('Inserting daily result to db')
    cons.insert_daily_result(db=db, entities=result)
    logger.debug('Data successfully inserted')


class Processor:
    def __init__(self, country):
        self.country, self.lang, self.nlp, self.ent, self.pipes \
            = language_manager(country=country)

    def process_daily_data(self, db: Session, date: datetime.date = datetime.date.today()):
        logger.debug('Getting data from db')
        data = title.get_daily_titles_by_lang_and_country(db=db,
                                                          date=date,
                                                          lang=self.lang,
                                                          country=self.country)
        logger.debug('Extracting entities')
        entities = self._entity_extractor(data)
        logger.debug('Calculating most common')
        common_entity_names = (
            self._accept_frequency(entity, frequency, date)
            for entity, frequency, date
            in self.entity_generator(entities, date=date)
        )
        common_entity_names = {k: v for k, v in common_entity_names}
        common_entities_with_id = self._common_entities_intersection(entities, common_entity_names)

        # print(common_entities_with_id)
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
                          frequencies: dict,
                          date: datetime.date):
        """Для каждой сущности и имени сущности считаем количество повторений,
         -> строим облако слов и выделяем 10 самых распространенных"""
        build_wordcloud(entity=entity,
                        frequencies=frequencies,
                        date=date,
                        country=self.country,
                        ent_mapper=self.ent)
        return self._most_common_entity_names(entity=entity, frequencies=frequencies)

    @staticmethod
    def _most_common_entity_names(entity: str, frequencies: dict):
        sorted_freq = sorted(frequencies, key=frequencies.get, reverse=True)
        return entity, sorted_freq[:10]

    def _entity_extractor(self, data: CursorResult):
        """Извлекаем список сущностей (по категориям) из текста и
        ассоциируем с каждой стрОки(id), в которых она упоминается"""
        entities: ENT = {ent: defaultdict() for ent in self.ent}
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


# from nlp_data.db.connection import DatabaseSession

# with DatabaseSession() as db:
#     process(db)
#     pass
    # process_daily_data(db=db, date=day)
    # do_some_shit(db=db, date=day)
    # get_daily_results(db=db, date=day, country='Russia')
