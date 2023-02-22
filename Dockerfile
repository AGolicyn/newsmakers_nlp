FROM python:3.10-buster

WORKDIR /src/nlp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./src/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python -m spacy download en_core_web_lg
RUN python -m spacy download de_core_news_lg
RUN python -m spacy download ru_core_news_lg

COPY ./src .


