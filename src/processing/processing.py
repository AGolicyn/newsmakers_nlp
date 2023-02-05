import time

import jsonlines
import sys
import unicodedata

import googletrans
from googletrans import Translator
import numpy as np
# nltk.download('punkt')
# nltk.download('stopwords')
import pandas as pd
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def process(raw_data):
    time.sleep(1)
    return {"val": True}


raw_data = []

# print(googletrans.LANGUAGES)
# translator = Translator()
# result = translator(raw_data, src='ru')
# print(raw_data)
#
# text_data = np.array(raw_data)
# punctuation_digit = dict.fromkeys(
#     i for i in range(sys.maxunicode)
#     if unicodedata.category(chr(i)).startswith('P')
#     or unicodedata.category(chr(i)).startswith('Nd')
# )
#
# stop_words = stopwords.words('russian')
# stop_words.extend(['млн', 'млрд', 'руб', 'новость', 'тыс', 'кв', 'год', 'года', 'году', 'рбк', 'также',
#                    'это', 'эта', 'эти', 'по', 'который', 'январь', 'февраль', 'март', 'апрель', 'май',
#                    'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь', 'аиф', 'фото'
#                    'редакция', 'газета', 'фгб', 'раздел', 'видео', 'почему'])
#
# morph = pymorphy2.MorphAnalyzer()
#
# new_text_data = []
# for i, text in enumerate(text_data):
#     # cast punctuation and digits to None
#     new_text = ''.join([char.translate(punctuation_digit) for char in text])
#     tokenized_words = [morph.parse(word)[0].normal_form for word in word_tokenize(new_text)]
#     new_text_data.append(' '.join([word for word in tokenized_words if word not in stop_words]))
# new_text_data = np.array(new_text_data)
#
# tfidf = TfidfVectorizer(ngram_range=(3, 3))
# feature_matrix = tfidf.fit_transform(new_text_data)
# frame = pd.DataFrame(feature_matrix.todense(), columns=tfidf.get_feature_names_out())
#
# # print(frame.max().sort_values(ascending=False)[:20])
# a = frame.max().sort_values(ascending=False)[:20]
# b = list(a.axes)[0]
# # print(set.intersection(set(b[0].split()), set(b[1].split())))
# res = []
# temp = [x for i,x in enumerate(b) for j,y in enumerate(b)
#         if len(set.intersection(set(x.split()), set(y.split()))) > 2]
# print(set(temp))
# set_collection = [set(result.split()) for result in b]
# cols = [set_collection[0]]
# for first_set in set_collection:
#     for second_set in set_collection:
#         if len(set.intersection(first_set, second_set)) < 2:
#             cols.append(second_set)
#             set_collection.remove(second_set)
#
#
# print(cols)

# print(list(frame.max().sort_values(ascending=False)[:20]))
# print(feature_matrix.max())


