"""
DATA601
Joshua Black
Objective measures for NB2 LDA models.
"""

from gensim.models.coherencemodel import CoherenceModel
from gensim.models import LdaMulticore
from gensim import corpora

import numpy as np
import pandas as pd

import NL_helpers
import NL_topicmodels

philoso_df = pd.read_pickle('pickles/nb2_v2_philoso_df.tar.gz')
philoso_df['Tokenised'] = philoso_df['Text'].apply(NL_helpers.tokenise_and_stop)
dictionary = corpora.Dictionary.load('dictionaries/nb2_v2_philoso.dict')
philoso_corpus = NL_topicmodels.NL_corpus(philoso_df, dictionary)

model = LdaMulticore.load('lda_models/nb2_v2_philoso_100.ldamodel')

measures = pd.DataFrame()
for i in [10, 50, 100, 500]:
    model = LdaMulticore.load(f'lda_models/nb2_v2_philoso_{i}.ldamodel')
    log_perp = model.log_perplexity(philoso_corpus, total_docs=220)
    cm = CoherenceModel(model=model, texts=philoso_corpus,
        dictionary=philoso_corpus.dictionary, coherence='c_v')
    coherence = cm.get_coherence()
    measures = measures.append(pd.Series([i, log_perp, coherence]), ignore_index=True)
measures.columns = ['Topics', 'Log Perplexity', 'Coherence (C_V)']
measures.to_csv('all_measures.csv')
measures
