import uuid
from enum import Enum
import spacy
from collections import namedtuple
from collections import defaultdict

ENT: dict[str, defaultdict[str, list[uuid]]]

SUPPORTED_COUNTRIES = ['Russia', 'USA', 'Germany']

class Entity(Enum):
    Location = 'LOC'
    Person = 'PER'
    Organization = 'ORG'


Lang = namedtuple('NLP', 'country lang nlp entities pipes')
def language_manager(country: str) -> namedtuple:
    if country == 'Russia':
        return Lang(country='Russia',
                    lang='RU',
                    nlp=spacy.load("ru_core_news_lg"),
                    entities={'LOC': Entity.Location.value,
                              'PER': Entity.Person.value,
                              'ORG': Entity.Organization.value},
                    pipes=["ner", 'lemmatizer', 'attribute_ruler', 'parser'])
                           # 'morphologizer', ])
    elif country == 'USA':
        return Lang(country='USA',
                    lang='EN',
                    nlp=spacy.load("en_core_web_lg"),
                    entities={'GPE': Entity.Location.value,
                              'PERSON': Entity.Person.value,
                              'ORG': Entity.Organization.value},
                    pipes=["ner", 'lemmatizer', 'tagger', 'attribute_ruler'])
    elif country == 'Germany':
        return Lang(country='Germany',
                    lang='DE',
                    nlp=spacy.load("de_core_news_lg"),
                    entities={'LOC': Entity.Location.value,
                              'PER': Entity.Person.value,
                              'ORG': Entity.Organization.value},
                    pipes=["ner", 'lemmatizer', 'morphologizer', 'attribute_ruler'])
    else:
        raise f'{country} NOT IMPLEMENTED'

import os
import pathlib
p = pathlib.Path('..')
# print(p.cwd())
# print(Entity.Location.value)