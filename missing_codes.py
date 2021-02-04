# Look in to ST_18800924_ARTICLE14 and ME_18940605_ARTICLE7 and TT_18710720_ARTICLE23; wood: ODT_18881108_ARTICLE3;

import re
import os
import pandas as pd
import NL_helpers

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'
MISSING = [
    'ST_18800924_ARTICLE14',
    'ME_18940605_ARTICLE7',
    'TT_18710720_ARTICLE23',
    'ODT_18881108_ARTICLE3',
    'OW_18810604_ARTICLE108'
]

filtered_dfs = []
for i in range(9):
    print(i)
    df = pd.read_pickle(DATASET_PATH+f'corpus_df_{i}.tar.gz')
    try:
        filtered_df = df.loc[df.index.intersection(MISSING)]
        filtered_dfs.append(filtered_df)
    except KeyError:
        pass
    del df


missing_df = pd.concat(filtered_dfs)
missing_df = missing_df[~missing_df.astype(str).duplicated()]
missing_df
[article_code for article_code in MISSING if not article_code in missing_df.index]

from multiprocessing import Pool
slices_directory = '/home/joshua/Documents/data601_small_slices/'
slices = [f'{slices_directory}{path}' for path in os.listdir(slices_directory)]

def phil_from_slice(slice_path):
    df = pd.read_pickle(slice_path)
    try:
        phil = df.loc[df.index.intersection(MISSING)]
    except KeyError:
        phil = pd.DataFrame(columns=df.columns)
    del df
    return phil

df_collector = []
if __name__ == '__main__':
    with Pool(processes=os.cpu_count()//4) as pool:
        missing_sheep = pool.imap(phil_from_slice, slices)
        for sheep in missing_sheep:
            df_collector.append(sheep)
df = pd.concat(df_collector)

df
df = df[~df.astype(str).duplicated()]
df

import pickle
import NL_helpers

with open('classifiers/NB_2_v2.pickle', 'rb') as fin:
  phil_classifier_2 = pickle.load(fin)

series = (
    df['Text']
    .map(NL_helpers.blocks2string)
)
predictions = pd.Series(data=phil_classifier_2.predict(series))
predictions
series

df['Text'] = df['Text'].map(filter_short_articles)
df

def filter_short_articles(string):
    if len(string)<800:
        string = ''
    return string


nb2_corpus = pd.read_pickle('pickles/nb2_philoso_df_v2.tar.gz')
nb2_corpus.loc['ME_18940605_ARTICLE7']
