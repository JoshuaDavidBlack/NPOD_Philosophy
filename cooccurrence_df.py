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
    elif stat == 'ml':
        function = NL_helpers.ml_coocs

    for term in search_terms:
        try:
            coocs = function(term, dtm, ttm, num_coocs=NUM_COOCS)
            cooc_df.loc[f'{term}_{stat}'] = coocs.index.to_series().append(coocs, ignore_index=True).to_list()
            for i in coocs.index:
                if not f'{i}_{stat}' in cooc_df.index:
                    secondary_coocs = function(i, dtm, ttm, num_coocs=NUM_COOCS)
                    cooc_df.loc[f'{i}_{stat}'] = secondary_coocs.index.to_series().append(secondary_coocs, ignore_index=True).to_list()
        except KeyError:
            print(f'{term} not in dictionary')

search_terms = [
    'philosophy',
    'theology',
    'speculative',
    'ethics',
    'metaphysics',
    'theosophy',
    'materialism',
    'idealism',
    'liberalism',
    'socialism',
    'stout',
    'freethinker'
]

NUM_COOCS = 50

dtm = pd.read_pickle('pickles/dtm_aggressive_16kwords.tar.gz')
ttm = pd.read_pickle('pickles/tt_agressive_16kwords.pickle')

cooc_df = pd.DataFrame(columns = [f'Term {i}' for i in range(NUM_COOCS)] + [f'Score {i}' for i in range(NUM_COOCS)])

stats = ['log dice', 'ml']

for stat in stats:
    populate_df(cooc_df, stat, search_terms)



print(f'time taken: {time.time()-t0}')


cooc_df

cooc_df.to_pickle('pickles/cooc_df.pickle')


del dtm, ttm

to_be_generated = [
    'BOW_entities',
    'TF-IDF_entities',
    'BOW_propn',
    'TF-IDF_propn',
    'TF-IDF_25kwords'
]

entity_terms = [
    'plato',
    'stout',
    'theosophy',
    'university',
    'canterbury college',
    'the new zealand institute',
    'the church',
    'new zealand'
]

propn_terms = [
    'Besant',
    'Stout',
    'Vogel',
    'Plato',
    'Aristotle',
    'Spencer',
    'Carlyle',
    'Darwin',
    'Hosking',
    'Worthington',
    'Collins'
]

for variety in to_be_generated:
    if variety == 'TF-IDF_25kwords':
        keywords = search_terms
    elif variety.endswith('entities'):
        keywords = entity_terms
    elif variety.endswith('propn'):
        keywords = propn_terms
    dtm = pd.read_pickle(f'pickles/dtm_{variety}.tar.gz')
    ttm = pd.read_pickle(f'pickles/ttm_{variety}.tar.gz')
    cooc_df = pd.DataFrame(columns = [f'Term {i}' for i in range(NUM_COOCS)] + [f'Score {i}' for i in range(NUM_COOCS)])
    stats = ['log dice', 'ml']
    for stat in stats:
        populate_df(cooc_df, stat, keywords)
    cooc_df.to_pickle(f'pickles/cooc_{variety}_df.tar.gz')
    del dtm, ttm
