import pandas as pd
import os
import glob
import re
from NL_helpers import *
from NL_topicmodels import *

# PATH = "/home/joshua/Documents/Academic/MADS/DATA601/NPOD_Starter/"
PATH = "/home/joshua/hdd/Documents/MADS/DATA601/NPOD_Starter/"
DS_PATH = '/home/joshua/hdd/Datasets/papers-past/'

path_walk = os.walk(DS_PATH)

# Collect issue folders using regex
issue_directories = {}
for location in path_walk:
    match = re.search("[A-Z]*_\d{8}$", location[0])
    if match:
        issue_directories[match.group(0)] = location[0] + '/'
issue_directories


corpus_dict = {}
for issue, directory in issue_directories.items():
    newspaper = issue[:-9]
    date = issue[-8:]
    articles = issue2articles(directory)
    for article_code, title_and_text in articles.items():
        article_code = article_code[7:] # remove 'MODSMD_' from article code
        item_id = '_'.join([issue, article_code])
        title, text = title_and_text
        tokenised_and_stopped = tokenise_and_stop(text)
        corpus_dict[item_id] = (
            newspaper,
            date,
            title,
            text,
            tokenised_and_stopped
            )

corpus_df = pd.DataFrame.from_dict(
    corpus_dict,
    orient='index',
    dtype = object,
    columns=['Newspaper', 'Date', 'Title', 'Text', 'Tokenised']
    )


cutoff = 20
filtered_corpus_df = corpus_df[corpus_df['Tokenised'].apply(lambda x: len(x) >= cutoff)]

minimum_in_docs = 5
dictionary = corpora.Dictionary(filtered_corpus_df['Tokenised'])
dictionary.filter_extremes(no_below=minimum_in_docs, no_above=0.5)
dictionary.compactify()

type(filtered_corpus_df['Tokenised'][0])

starter_corpus = NL_corpus(filtered_corpus_df, dictionary)
starter_corpus.items

len(starter_corpus.items)

starter_corpus.items = starter_corpus.items[starter_corpus.items['BOW'].apply(lambda x: len(x) >= cutoff)]

len(starter_corpus.items)
# Perhaps this is the point to do the filtering

test_model = LdaMulticore(
    starter_corpus,
    num_topics=10,
    workers = 15,
    chunksize = 220,
    id2word=starter_corpus.dictionary,
    iterations = 500,
    passes = 25,
    eval_every = 100
)

test_model.show_topics(20)

##### Gonna do a test topic model too.
from gensim import corpora
from gensim.models import LdaMulticore
import pyLDAvis.gensim
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import logging
logging.basicConfig(filename='first_test.log', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

tokenizer = RegexpTokenizer(r"\w[\w\']+\w")
stops = set(stopwords.words())

starter_corpus = []
for v in corpus_dict.values():
    total_string = ' '.join(v[2])
    tokens = tokenizer.tokenize(total_string.lower())
    stopped_tokens = [i for i in tokens if not i in stops]
    starter_corpus.append(stopped_tokens)

minimum_in_docs = 5

dictionary = corpora.Dictionary(starter_corpus)
dictionary.filter_extremes(no_below=minimum_in_docs, no_above=0.5)
dictionary.compactify()

corpus_bow = []
for text in starter_corpus:
    bag = dictionary.doc2bow(text)
    corpus_bow.append(bag)

models = []
for i in [25, 50, 100, 150]:
    starter_model = LdaMulticore(corpus_bow,
        num_topics=i,
        workers = 15,
        chunksize = 220,
        id2word=dictionary,
        iterations = 500,
        passes = 25,
        eval_every = 100
        )
    models.append(starter_model)
    starter_model.save('lda_models/starter_'+str(i))

import pyLDAvis.gensim

for i, model in enumerate(models):
    vis = pyLDAvis.gensim.prepare(model, starter_corpus, dictionary=dictionary)
    pyLDAvis.save_html(vis, f'starter_LDAvis_{i}.html')


###############


from nltk.corpus import brown, stopwords
from nltk.tokenize import RegexpTokenizer
from gensim import corpora

class NL_corpus():
    """
    Corpus class for use with gensim for topic modelling.

    Input: 1) pandas dataframe containing 'Tokenised' column with
    tokenised texts for each article.
        2) Dictionary for use with gensim.

    Main benefit is use of iterator method.
    """

    def __init__(self, corpus_df, dictionary):
        self.items = corpus_df
        self.dictionary = dictionary
        self.generate_bow()

    def __iter__(self):
        for bag in self.items['BOW']:
            yield bag

    def generate_bow(self):
        """
        Generates bag of words representation of tokenised text and adds
        it to item dataframe as column 'BOW'.
        """
        bags = {}
        for index, value in self.items.iterrows():
            tokenised = value[4]
            bags[index] = [self.dictionary.doc2bow(tokenised)]
        bags_df = pd.DataFrame.from_dict(
            bags,
            orient='index',
            dtype = object,
            columns=['BOW']
            )
        self.items = self.items.join(bags_df)
