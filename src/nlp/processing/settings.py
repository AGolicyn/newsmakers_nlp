import pickle
import time
import uuid
from enum import Enum
import spacy
from spacy import Language
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
                    nlp=_load_nlp('RU'),
                    entities={'LOC': Entity.Location.value,
                              'PER': Entity.Person.value,
                              'ORG': Entity.Organization.value},
                    pipes=["ner", 'lemmatizer', 'attribute_ruler', 'parser'])
                           # 'morphologizer', ])
    elif country == 'USA':
        return Lang(country='USA',
                    lang='EN',
                    nlp=_load_nlp('EN'),
                    entities={'GPE': Entity.Location.value,
                              'PERSON': Entity.Person.value,
                              'ORG': Entity.Organization.value},
                    pipes=["ner", 'lemmatizer', 'tagger', 'attribute_ruler'])
    elif country == 'Germany':
        return Lang(country='Germany',
                    lang='DE',
                    nlp=_load_nlp('DE'),
                    # nlp=spacy.load("de_core_news_md"),
                    entities={'LOC': Entity.Location.value,
                              'PER': Entity.Person.value,
                              'ORG': Entity.Organization.value},
                    pipes=["ner", 'lemmatizer', 'parser', 'attribute_ruler'])
    else:
        raise f'{country} NOT IMPLEMENTED'


def _load_nlp(lang: str):
    if lang == 'RU':
        with open('/src/nlp/processing/nlp_data/ru_core_news_md.pickle', 'rb') as f:
            ru_nlp = pickle.load(f)
        return ru_nlp
    elif lang == 'EN':
        with open('/src/nlp/processing/nlp_data/en_core_web_md.pickle', 'rb') as f:
            en_nlp = pickle.load(f)
        return en_nlp
    elif lang == 'DE':
        with open('/src/nlp/processing/nlp_data/de_core_news_md.pickle', 'rb') as f:
            de_nlp = pickle.load(f)
        return de_nlp
    else:
        raise f'NLP for {lang} NOT INSTALLED'
import os
import pathlib
p = pathlib.Path('..')
print(p.cwd())
# print(Entity.Location.value)

# nlp_2 = spacy.load("en_core_web_lg")
# nlp_3 = spacy.load("de_core_news_lg")




# nlp_1 = spacy.load("de_core_news_lg")
# print(nlp_1)
# nlp_1.to_disk('ru_core_news_lg')
# time.sleep(2)

# ru_nlp = Language()
# ru_nlp.from_disk(path='./ru_core_news_lg')
# print(my_nlp)

# with open('nlp_data/de_core_news_md.pickle', 'wb') as f:
#     pickle.dump(nlp_1, f)
#
# with open('nlp_data/en_core_web_lg.pickle', 'wb') as f:
#     pickle.dump(nlp_2, f)
#
# with open('nlp_data/de_core_news_lg.pickle', 'wb') as f:
#     pickle.dump(nlp_1, f)



# with open('nlp_data/ru_core_news_md.pickle', 'rb') as f:
#     ru = pickle.load(f)
# with open('nlp_data/en_core_web_lg.pickle', 'rb') as f:
#     en = pickle.load(f)
# with open('nlp_data/de_core_news_lg.pickle', 'rb') as f:
#     de = pickle.load(f)


# print(nlp_1, ru)
# print(nlp_2, en)
# print(nlp_3, de)