# <md>
# # DATA601
# Joshua Black
# ## Starter Kit Experiments in Processing and Initial Filtering.
# This notebook presents initial attempts at processing the National Library
# newspaper data, the result of using topic models to find genres
# of writing interesting for investigating philosophical writing within the
# 'starter kit' corpus and for finding the topics covered within those genres.

# <md>
# ## The Starter Pack
# The Starter Pack is around 2GB uncompressed and contains articles from
# - Charleston argus.
# - Hot lakes chronicle.
# - Lyell times and Central Buller gazette.
# - Mt. Benger mail.
# - The New Zealand gazette and Wellington spectator.
# - The Oxford observer : and Canterbury democrat.
# - Victoria times.

# <md>
# ## Initial Processing
# The Starter Pack is given uncompressed. This is not true of the full dataset
# and will require a slightly different method.
#
# We begin by importing my helper functions and reading through the Starter Pack
# directories to find top-level folders for each issue in the Starter Pack.

# <codecell>

import sys
import os
import glob
import re

# Remove before exporting notebook
sys.path.append('/home/joshua/hdd/Documents/MADS/DATA601/')

import pandas as pd

from NL_helpers import *
from NL_topicmodels import *

PATH = "/home/joshua/hdd/Documents/MADS/DATA601/NPOD_Starter/"

# <codecell>
path_walk = os.walk(PATH)

# Collect issue folders using regex. All are of form NEWSPAPERCODE_DATE,
# where date is in format YYYYMMDD
issue_directories = {}
for location in path_walk:
    match = re.search("[A-Z]*_\d{8}$", location[0])
    if match:
        issue_directories[match.group(0)] = location[0] + '/'

# <md>
# Having collected the directories for each issue, we can collect the
# information we want from each. In this case, we parse the XML to produce
# a Python dictionary with an article id as key, and the newspaper, date,
# title, text, and tokenised text as values.
#
# The raw text is given as a list of strings, where each string corresponds to
# a 'text block' in the original newspaper scans. The tokenised text
# is tokenised the python NLTK regex tokeniser and default NLTK list of
# stopwords.

# <codecell>
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

# <md>
# We now convert this dictionary to a pandas dataframe. We use the object datatype
# in order store Python lists within it. We save it as a pickle, also to enable
# storage which respects Python datatypes.

# <codecell>
corpus_df = pd.DataFrame.from_dict(
    corpus_dict,
    orient='index',
    dtype = object,
    columns=['Newspaper', 'Date', 'Title', 'Text', 'Tokenised']
    )

pickle_dir = '/home/joshua/hdd/Documents/MADS/DATA601/pickles/'
corpus_df.to_pickle(pickle_dir + 'Starter_Items.tar.gz')
corpus_df # Hydrogen (+atom text editor) doesn't support exporting output with .ipynb
# <md>
# With output:
# 	Newspaper	Date	Title	Text	Tokenised
# CHARG_18670302_ARTICLE1	CHARG	18670302	UNTITLED	[ago a till last Thurs- with 40oz. of gold and...	[ago, last, thurs, 40oz, gold, went, back, sma...
# CHARG_18670309_ARTICLE1	CHARG	18670309	UNKNOWN	[1.33 2.25 3.15 2.—Halcyon, s.s., Wing, master...	[halcyon, wing, master, jane, schooner, julia,...
# CHARG_18670309_ARTICLE2	CHARG	18670309	CHARLESTON ARGUS.	[If the Pakihi district was but well supplied ...	[pakihi, district, well, supplied, water, nut,...
# CHARG_18670309_ARTICLE3	CHARG	18670309	UNTITLED	[Some little excitement has been evinced in re...	[little, excitement, evinced, reference, tramw...
# CHARG_18670309_ARTICLE4	CHARG	18670309	SATURDAY, MARCH 9, 1867. UNKNOWN	[3/u^ (Before C. Broad, Larceny. Ann Connelly,...	[broad, larceny, ann, connelly, woman, charged...
# ...	...	...	...	...	...
# VT_18410915_ARTICLE1	VT	18410915	Wellington Tavern.	[Edward Davis begs to inform his friends and t...	[edward, davis, begs, inform, friends, public,...
# VT_18410915_ARTICLE2	VT	18410915	UNTITLED	[Messrs Pratt and Bevan beg respectfully to in...	[messrs, pratt, bevan, beg, respectfully, info...
# VT_18410915_ARTICLE3	VT	18410915	UNTITLED	[We insert the following communication by, par...	[insert, following, communication, partic, ula...
# VT_18410915_ARTICLE4	VT	18410915	UNTITLED	[The following Particulars were composed a sel...	[following, particulars, composed, selected, m...
# VT_18410915_ARTICLE5	VT	18410915	PLAN of THE CITY OF WELLINGTON Port Nicholson ...	[]	[]
#
# 11516 rows × 5 columns


# <md>
# ## Initial Topic Model Using Gensim
# Earlier experiments have shown that having a bunch of empty documents around
# is not good for producing interesting models. I found an interesting looking
# topic filled with words in te reo, but was disappointed to find it represented
# a very small number of actual documents and a huge number of empty ones.
# I will use two filtering steps. First, I filter out those articles which
# have less than 20 words after tokenising.

# <codecell>
cutoff = 20
filtered_corpus_df = corpus_df[corpus_df['Tokenised'].apply(lambda x: len(x) >= cutoff)]

# <md>
# We then create a dictionary for applying topic models with Gensim.
