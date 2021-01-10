import re
import os
import pandas as pd
import NL_helpers

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'
SLICE_PATH = '/home/joshua/Documents/data601_small_slices/'
FILTER_STRING = 'philoso*'

for i in range(9):
    print(i)
    df = pd.read_pickle(DATASET_PATH+f'corpus_df_{i}.tar.gz')
    small_slice_size = 100000
    slices = len(df)//small_slice_size
    for j in range(slices):
        df.iloc[j*small_slice_size:(j+1)*small_slice_size].to_pickle(f'{SLICE_PATH}corpus_df{i}_slice{j}.tar.gz')
    del df
