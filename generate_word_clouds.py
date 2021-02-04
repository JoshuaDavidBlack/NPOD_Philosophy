"""
Generate word clouds for:
  * A sample of 10000 articles from the whole dataset
  * The `philoso*' corpus
  * The nb1 corpus
  * The nb2 corpus
  * The rel-sci corpus

 In each case, a random sample of 10000 articles will be used.
"""

import pandas as pd
import wordcloud

from gensim.models import TfidfModel
from gensim.matutils import corpus2csc

import NL_helpers
import NL_topicmodels

corpora = [
    'corpus_10000_subset',
    'philoso',
    'nb1_philoso',
    'nb2_v2_philoso',
    'rel_v2_philoso'
]

for corpus in corpora:

    # Load (sample of) corpus and dictionary
    df = pd.read_pickle(f'pickles/{corpus}_df.tar.gz')
    df = df.sample(n=10000, random_state=1)
    df['Tokenised'] = df['Text'].apply(NL_helpers.tokenise_and_stop)
    dictionary = NL_topicmodels.get_dictionary(
        df,
        corpus + '_10k_sample',
        min_in=50,
        max_prop=0.2
    )
    gensim_corpus = NL_topicmodels.NL_corpus(df, dictionary)
    tfidf_model = TfidfModel(
        gensim_corpus,
        dictionary=gensim_corpus.dictionary
    )
    gensim_corpus.items['TF-IDF'] = tfidf_model[gensim_corpus]

    # Create document term matrix.
    dtm = corpus2csc(gensim_corpus.items['TF-IDF'])
    del df, gensim_corpus
    dtm = pd.DataFrame.sparse.from_spmatrix(dtm)
    dtm.index = dictionary.values()

    # Sum accross columns to get corpus word counts.
    word_counts = dtm.sum(axis=1)
    del dtm
    word_counts.to_csv(f'csv/{corpus}_word_counts_tf-idf.csv')

    # Use corpus word count to generate word cloud and save.
    word_counts = word_counts.to_dict()
    wordcloud_image = wordcloud.WordCloud(
        mode='RGBA',
        background_color=None,
        width=1000,
        height=500)
    wordcloud_image = wordcloud_image.generate_from_frequencies(word_counts)
    wordcloud_image.to_file(f'wordclouds/{corpus}_tf-idf.png')
