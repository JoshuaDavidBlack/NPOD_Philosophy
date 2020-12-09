"""
topics_and_docs.py
Joshua Black
Most representative documents for each topic.
Dominant topic for each document.
"""

import os
os.chdir('/home/joshua/hdd/Documents/MADS/DATA601/HelperScripts/')
from produce_sheets import *

# Needed to evaluate 'Text' in DF as python list.
import ast

from gensim.models.coherencemodel import CoherenceModel
from gensim.models import LdaMulticore
from gensim import corpora

import numpy as np
import pandas as pd

# Load corpus dataframe
corpus_df = pd.read_csv('Starter_DF.csv', index_col=0)

corpus_df

### Recreate corpus dictionary etc.

from gensim import corpora
from gensim.models import LdaMulticore
import pyLDAvis.gensim
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r"\w[\w\']+\w")
stops = set(stopwords.words())


starter_corpus = []
for v in corpus_df['Text']:
    total_string = ' '.join(ast.literal_eval(v))
    tokens = tokenizer.tokenize(total_string.lower())
    stopped_tokens = [i for i in tokens if not i in stops]
    starter_corpus.append(stopped_tokens)

minimum_in_docs = 5

dictionary = corpora.Dictionary(starter_corpus)
dictionary.filter_extremes(no_below=minimum_in_docs, no_above=0.5)
dictionary.compactify()

# Save dictionary while at it
dictionary.save('lda_models/Starter_dict')

corpus_bow = []
for text in starter_corpus:
    bag = dictionary.doc2bow(text)
    corpus_bow.append(bag)


###

# Load monist model

sizes = [25, 50, 100, 150]
models = []
for s in sizes:
    model = LdaMulticore.load(f'lda_models/starter_{s}')
    models.append(model)

for i, model in enumerate(models):
    docs_df = docs_by_topic(model, corpus_df, corpus_bow)
    docs_df.to_csv(f'lda_models/Starter_{i}_docs.csv')

# Documents by dominant topic.
# See: https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#14computemodelperplexityandcoherencescore
def docs_by_topic(model, corpus_df, corpus_bow):
    sent_topics_df = pd.DataFrame()
    for i, row in enumerate(model[corpus_bow]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = model.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant Topic', 'Perc Contribution', 'Topic Keywords']

    sent_topics_df.index = corpus_df.index

    enriched_items_df = corpus_df.join(sent_topics_df)
    return enriched_items_df


# Topics by most representative member: # <- This is no good.
grouped_items_df = enriched_items_df.groupby('Dominant Topic')
rep_docs = pd.DataFrame()
topic_sizes = []
for i, grp in grouped_items_df:
    rep_docs = pd.concat([rep_docs, grp.sort_values(['Perc Contribution'],
        ascending=[0]).head(1)], axis=0)
    topic_sizes.append(grp.count()[0])
rep_docs['Topic Size'] = topic_sizes

rep_docs.columns

rep_docs.to_csv('rep_docs_all_30.csv')
rep_docs[['Dominant Topic', 'Topic Size', 'Perc Contribution', 'Title', 'Journal ID', 'Year']]
