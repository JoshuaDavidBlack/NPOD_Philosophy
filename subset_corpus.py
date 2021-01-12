import re
import os
import pandas as pd
import NL_helpers

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'

filtered_dfs = []
for i in range(9):
    print(i)
    df = pd.read_pickle(DATASET_PATH+f'corpus_df_{i}.tar.gz')
    filtered_df = df.sample(n=2000)
    filtered_dfs.append(filtered_df)
    del df


keyword_df = pd.concat(filtered_dfs)
keyword_df = keyword_df[~keyword_df.astype(str).duplicated()]

keyword_df.to_pickle(DATASET_PATH + 'corpus_2000per_subset_df.pickle')
