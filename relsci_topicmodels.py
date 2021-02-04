"""
Generate topic models for rel-sci corpus.
"""

import sys
import os
import glob
import re
import logging
logging.basicConfig(
    filename='lda_models.log',
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO
)
from smart_open import open

import pandas as pd

from gensim.models import LdaMulticore
from gensim import corpora

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import NL_helpers
import NL_topicmodels

TOKENIZER = RegexpTokenizer(r"\w[\w\']+\w")
STOPS = set(stopwords.words())

def fit_and_save_models(corpus, corpus_name, num_topics):
    """Code to fit model for corpus with given numbers of topics (iterable).

    Naming convention ignores that the number of topics is *also* a
    hyperparameter.
    """

    # Fit model
    for num_topics in num_topics:
        lda_model = LdaMulticore(
            corpus,
            num_topics= num_topics,
            workers = 15, # real cores - 1
            chunksize = 500,
            id2word=corpus.dictionary,
            iterations = 500,
            passes = 25,
            eval_every = 100
        )

        # Save model
        lda_model.save(f'lda_models/{corpus_name}_{num_topics}.ldamodel')

        # Extract keywords for each topic, save a csv via pandas dataframe.
        topic_words = NL_topicmodels.topics_and_keywords(lda_model)
        topic_words_df = pd.DataFrame.from_dict(topic_words, orient='index')
        topic_words_df.to_csv(
            f'lda_models/{corpus_name}_{num_topics}.csv'
        )



def get_dictionary(corpus_df, corpus_name):
    """Given name of corpus, attempt to load pre-generated dictionary.
    If not dictionary present, generate one."""
    try:
        dictionary = corpora.Dictionary.load(
            f'dictionaries/{corpus_name}.dict'
        )
    except FileNotFoundError:
        minimum_in_docs = 10
        dictionary = corpora.Dictionary(corpus_df['Tokenised'])
        dictionary.filter_extremes(no_below=minimum_in_docs, no_above=0.4)
        dictionary.compactify()
        dictionary.save(f'dictionaries/{corpus_name}.dict')

    return dictionary



def main():
    """The main function."""
    corpus_names = ['rel_v2_philoso']
    num_topics = [10, 50, 100, 500]

    for corpus_name in corpus_names:
        if corpus_name in ['rel_philoso', 'rel_v2_philoso']:
            corpus = pd.read_pickle(f'pickles/{corpus_name}_df.tar.gz')
            corpus['Tokenised'] = corpus['Text'].apply(tokenise_and_stop)
            dictionary = get_dictionary(corpus, corpus_name)
            corpus = NL_topicmodels.NL_corpus(corpus, dictionary)
            fit_and_save_models(corpus, corpus_name, num_topics)
        elif corpus_name == 'nb1_philoso':
            dictionary = corpora.Dictionary.load(
                f'dictionaries/{corpus_name}.dict'
            )
            corpus = NL_topicmodels.NL_streamed_corpus(
                '/home/joshua/Documents/philoso_nb1/bags.csv',
                dictionary
            )
            fit_and_save_models(corpus, corpus_name, num_topics)



def tokenise_and_stop(text):
    """
    Given text as list of text blocks, returned text tokenized and
    stopped.
    """
    tokens = TOKENIZER.tokenize(' '.join(text).lower())
    stopped_tokens = [i for i in tokens if not i in STOPS]
    return stopped_tokens

main()

#
# corpus = pd.read_pickle(f'pickles/rel_philoso_df.tar.gz')
# corpus['Tokenised'] = corpus['Text'].apply(tokenise_and_stop)
# corpus
# dictionary = get_dictionary(corpus, corpus_name)
# corpus = NL_topicmodels.NL_corpus(corpus, dictionary)
