import re
import os
import pandas as pd
import NL_helpers

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'
FILTER_STRING = 'philoso*'

filtered_dfs = []
for i in range(9):
    print(i)
    df = pd.read_pickle(DATASET_PATH+f'corpus_df_{i}.tar.gz')
    filtered_df = df.loc[NL_helpers.search_text(df, FILTER_STRING),]
    filtered_dfs.append(filtered_df)
    del df


keyword_df = pd.concat(filtered_dfs)
keyword_df = keyword_df[~keyword_df.astype(str).duplicated()]

alphanumeric_filterstring = re.sub('\W', '', FILTER_STRING)
keyword_df.to_pickle(DATASET_PATH + f'{alphanumeric_filterstring}_df.tar.gz')

# Run to save a dataframe with one tenth of the rows in the larger dataframe.
# subset_df = keyword_df.sample(n=int(len(keyword_df)/10))
# subset_df.to_pickle(DATASET_PATH + f'{alphanumeric_filterstring}_sub_df.tar.gz')
