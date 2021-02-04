"""
For fast loading of cooccurence network for key words without need to
recalculate statistics.
Useful for presenting results without requiring too much computation.
"""

import time

import pandas as pd

import NL_helpers

t0 = time.time()

def populate_df(df, stat, search_terms):
    """Populate df of cooccurrences for list of search terms
    and their cooccurrences."""
    if stat == 'log dice':
        function = NL_helpers.log_dice_coocs
    elif stat == 'mi':
        function = NL_helpers.mi_coocs

    for term in search_terms:
        try:
            coocs = function(term, dtm, ttm, num_coocs=NUM_COOCS)
            cooc_df.loc[f'{term}_{stat}'] = (
                coocs
                .index
                .to_series()
                .append(coocs, ignore_index=True)
                .to_list()
            )
            for i in coocs.index:
                if not f'{i}_{stat}' in cooc_df.index:
                    secondary_coocs = function(i, dtm, ttm, num_coocs=NUM_COOCS)
                    cooc_df.loc[f'{i}_{stat}'] = (
                        secondary_coocs
                        .index
                        .to_series()
                        .append(secondary_coocs, ignore_index=True)
                        .to_list()
                    )
        except KeyError:
            print(f'{term} not in dictionary')

search_terms = [
    'philosophy',
    'theology',
    'evolutionary', #
    'darwin',
    'huxley',
    'conflict',
    'priestcraft',
    'ancestor',
    'primate',
    'monkey',
    'lower',
    'design',
    'designed',
    'heretic',
    'heresy',
    'creation',
    'creator', # Perhaps I should have stemmed these?
    'warfare',
    'evolution',
    'genesis',
    'human',
    'materialism',
    'theosophy',
    'salmond',
    'parker'
]

NUM_COOCS = 50


to_be_generated = [
    'part2_rel_TF-IDF',
    'part2_rel_BOW'
]

for variety in to_be_generated:
    keywords = search_terms
    dtm = pd.read_pickle(f'pickles/{variety}_dtm.tar.gz')
    ttm = pd.read_pickle(f'pickles/{variety}_ttm.tar.gz')
    cooc_df = pd.DataFrame(columns = [f'Term {i}' for i in range(NUM_COOCS)] + [f'Score {i}' for i in range(NUM_COOCS)])
    stats = ['log dice', 'mi']
    for stat in stats:
        populate_df(cooc_df, stat, keywords)
    cooc_df.to_pickle(f'pickles/cooc_{variety}_df.tar.gz')
    del dtm, ttm
