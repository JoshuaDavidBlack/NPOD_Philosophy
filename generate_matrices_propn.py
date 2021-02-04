# TODO: some functional decomposition

import logging
import re

import pandas as pd

from gensim import corpora
from gensim.models import TfidfModel
from gensim.matutils import corpus2csc

import NL_helpers
import NL_topicmodels

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

IN_NAME = 'pickles/rel_v2_propn_df.tar.gz' # 'pickles/philoso_propn_df.tar.gz'
OUT_PREFIX = 'rel_v2'

# Load dataset

philoso_df = pd.read_pickle(IN_NAME)

# Filter Spacy output

philoso_df['Proper Nouns'] = philoso_df['Proper Nouns'].map(
    lambda x: NL_helpers.filter_propns(x)
)

# Generate dictionary

minimum_in_docs = 5 # 10
max_prop = 0.5
dictionary = corpora.Dictionary(philoso_df['Proper Nouns'])
dictionary.filter_extremes(no_below=minimum_in_docs, no_above=max_prop)
dictionary.compactify()

# Generate bag of words rep

philoso_df['BOW'] = philoso_df['Proper Nouns'].apply(
    lambda x : dictionary.doc2bow(x)
)

# Generate TF-IDF rep
philoso_corpus = NL_topicmodels.NL_corpus(philoso_df, dictionary)
tfidf_model = TfidfModel(philoso_corpus, dictionary=dictionary)
philoso_corpus.items['TF-IDF'] = tfidf_model[philoso_corpus]

# Generate 'BOW' dtm and ttm
sparse = corpus2csc(philoso_corpus.items['BOW'])
dtm = pd.DataFrame.sparse.from_spmatrix(sparse)
dtm.index = philoso_corpus.dictionary.values()
del sparse
dtm.to_pickle(f'pickles/dtm_{OUT_PREFIX}_BOW_propn.tar.gz')

ttm = dtm.dot(dtm.transpose())
ttm.to_pickle(f'pickles/ttm_{OUT_PREFIX}_BOW_propn.tar.gz')

del dtm, ttm

# Generate 'TF-IDF' dtm and ttm
sparse = corpus2csc(philoso_corpus.items['TF-IDF'])
dtm = pd.DataFrame.sparse.from_spmatrix(sparse)
dtm.index = philoso_corpus.dictionary.values()
del sparse
dtm.to_pickle(f'pickles/dtm_{OUT_PREFIX}_TF-IDF_propn.tar.gz')

ttm = dtm.dot(dtm.transpose())
ttm.to_pickle(f'pickles/ttm_{OUT_PREFIX}_TF-IDF_propn.tar.gz')

del dtm, ttm
