import pandas as pd

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'

article_count = 0
for i in range(9):
    print(i)
    df = pd.read_pickle(DATASET_PATH+f'corpus_df_{i}.tar.gz')
    df = df[~df.astype(str).duplicated()]
    article_count += len(df)
    del df

print(article_count)
