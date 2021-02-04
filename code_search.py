import os
os.chdir('/home/joshua/hdd/Documents/MADS/DATA601/')

import re
import os
import pandas as pd
import NL_helpers

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'
MISSING = [
    'AG_18990504_ARTICLE7',
    'CHP_18951209_ARTICLE55',
    'ESD_18851028_ARTICLE1',
    'ESD_18891218_ARTICLE59',
    'ESD_18960111_ARTICLE47',
    'GRA_18960522_ARTICLE19',
    'LT_18801016_ARTICLE32',
    'LWM_18950614_ARTICLE27',
    'ME_18870708_ARTICLE32',
    'NEM_18920606_ARTICLE29',
    'ODT_18850204_ARTICLE30',
    'ODT_18980407_ARTICLE89',
    'ODT_18981013_ARTICLE51',
    'OW_18770317_ARTICLE59'
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
missing_df
for i in missing_df.index:
    print(missing_df.loc[i]['Title'])
