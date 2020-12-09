import pandas as pd
import os
import glob
import re
from NL_helpers import *

# PATH = "/home/joshua/Documents/Academic/MADS/DATA601/NPOD_Starter/"
PATH = "/home/joshua/hdd/Documents/MADS/DATA601/NPOD_Starter/"


path_walk = os.walk(PATH)

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
    for article_code, article_text in articles.items():
        item_id = '_'.join([issue, article_code])
        corpus_dict[item_id] = (newspaper, date, article_text)

corpus_df = pd.DataFrame.from_dict(corpus_dict, orient='index', columns=['Newspaper', 'Date', 'Text'])
corpus_df

corpus_df.to_csv('Starter_DF.csv')

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
