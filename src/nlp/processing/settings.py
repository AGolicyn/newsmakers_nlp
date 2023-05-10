import spacy
from enum import Enum
from collections import namedtuple


SUPPORTED_COUNTRIES = ["Russia", "USA", "Germany", "UK"]


class Entity(Enum):
    Location = "LOC"
    Person = "PER"
    Organization = "ORG"


Lang = namedtuple("NLP", "country lang nlp entities pipes")


def language_manager(country: str) -> namedtuple:
    if country == "Russia":
        return Lang(
            country="Russia",
            lang="RU",
            nlp=spacy.load("ru_core_news_md"),
            entities={
                "LOC": Entity.Location.value,
                "PER": Entity.Person.value,
                "ORG": Entity.Organization.value,
            },
            pipes=["ner", "lemmatizer", "attribute_ruler", "parser"],
        )

    elif country == "USA":
        return Lang(
            country="USA",
            lang="EN",
            nlp=spacy.load("en_core_web_md"),
            entities={
                "GPE": Entity.Location.value,
                "PERSON": Entity.Person.value,
                "ORG": Entity.Organization.value,
            },
            pipes=["ner", "lemmatizer", "tagger", "attribute_ruler"],
        )
    elif country == "Germany":
        return Lang(
            country="Germany",
            lang="DE",
            nlp=spacy.load("de_core_news_md"),
            entities={
                "LOC": Entity.Location.value,
                "PER": Entity.Person.value,
                "ORG": Entity.Organization.value,
            },
            pipes=[
                "ner",
                "lemmatizer",
                "parser",
                "attribute_ruler",
                "tagger",
                "morphologizer",
            ],
        )
    elif country == "UK":
        return Lang(
            country="UK",
            lang="EN",
            nlp=spacy.load("en_core_web_md"),
            entities={
                "GPE": Entity.Location.value,
                "PERSON": Entity.Person.value,
                "ORG": Entity.Organization.value,
            },
            pipes=["ner", "lemmatizer", "tagger", "attribute_ruler"],
        )
    else:
        raise f"{country} NOT IMPLEMENTED"
