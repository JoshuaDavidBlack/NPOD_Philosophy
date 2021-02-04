"""
NL_helpers.py
Joshua Black
black.joshuda@gmail.com

Contains helper functions for usings NLOD dataset.
"""

import xml.etree.ElementTree as ET
import glob
import os.path
import re
import textwrap
import html
import ast

import pandas as pd
import numpy as np

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from IPython.display import HTML
from ipywidgets import interact, interactive, fixed, interact_manual

TOKENIZER = RegexpTokenizer(r"\w[\w\']+\w")
STOPS = set(stopwords.words())

NS = {'mets':'http://www.loc.gov/METS/'}

CYTOSCAPE_STYLESHEET = STYLESHEET = [
    {
        'selector': 'edge',
        'style': {
            'width': 'mapData(weight, 3, 6, 1, 3)',
            'line-color': 'silver'
        }
    },
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'width': 'mapData(size, 1, 10, 10, 20)',
            'height': 'mapData(size, 1, 10, 10, 20)'
        }
    },
    {
        'selector': 'label',
        'style': {
            'font-size': 6,
            'text-valign': 'center',
            'text-background-color': 'white',
            'text-background-opacity': 0.6,
            'text-background-padding': 1,
            'text-border-color': 'black',
            'text-border-opacity': 1,
            'text-border-width': 0.5
        }
    }
]


def issue2articles(filepath):
    """
    Given string containing filepath to issue, return plain text
    of articles contained in issue.

    Filepath should be to folder with name of form {publication code}_{date}.

    Output: One-member dictionary with issue name as key and dictionary
    of following form as value:
        {article_code_1 (string): [[text_block_1 (string)],
            [text_block_2 (string)], ...],
        article_code_2 (string): [[text_block_1 (string)],
            [text_block_2 (string)], ...], ...}
    """

    # All issue directories w/in the dataset seem to have a further directory
    # with name 'MM_01'. It is convenient to exclude this from calls to the
    # function.
    filepath = filepath + 'MM_01/'

    # Read in xml files. Return mets filepath and list of pages.
    mets, pages = read_dir(filepath)

    # Function to get list of articles and their text blocks from mets file.
    article_codes = mets2codes(mets)

    # Function to take article and textblock codes and return articles.
    all_articles = codes2texts(article_codes, pages)

    return all_articles



def read_dir(filepath):
    """
    Given directory ('filepath') of individual issue.
    Checks existence of mets file and returns its path along with
    a list of paths for each page file.
    """
    pages = list(glob.glob(filepath + '0*.xml'))
    if os.path.exists(filepath + 'mets.xml'):
        mets = filepath + 'mets.xml'
    else:
        print(f'No mets file found in {filepath}')
        mets = None

    return mets, pages



def mets2codes(metspath):
    """
    Given path to mets file, return text block codes for articles
    contained in mets file.

    Returns dictionary of article codes as keys,
    with a 2-tuple containing the article title
    and a list of corresponding text block codes as values.
    """

    mets_tree = ET.parse(metspath)
    mets_root = mets_tree.getroot()
    logical_structure = mets_root.find("./mets:structMap[@LABEL='Logical Structure']", NS)
    articles = logical_structure.findall(".//mets:div[@TYPE='ARTICLE']", NS)

    art_dict = {}
    for article in articles:

        attributes = article.attrib
        article_id = attributes['DMDID']
        article_title = attributes.get('LABEL', 'UNTITLED')

        text_blocks = article.findall(".//mets:div[@TYPE='TEXT']", NS)
        block_ids = []
        for block in text_blocks:
            area = block.find(".//mets:area", NS)
            block_id = area.attrib['BEGIN']
            block_ids.append(block_id)

        art_dict[article_id] = (article_title, block_ids)

    return art_dict



def codes2texts(article_codes, pages):
    """
    Given list of articles and their text block codes, and a list of
    the ALTO files for each page in the issue, return a dictionary
    with article codes as keys and a list of text blocks as
    strings as values.
    """

    page_roots = parse_pages(pages)

    texts_dict = {}
    for article_id in article_codes.keys():
        title, blocks = article_codes[article_id]
        text = []
        for block in blocks:
            end_loc = block.find('_')
            page_no = block[0:end_loc]
            page_root = page_roots[page_no]
            xml_block = page_root.find(f".//TextBlock[@ID='{block}']")
            block_strings = xml_block.findall('.//String')
            block_as_string = process_block(block_strings)
            text.append(block_as_string)
        texts_dict[article_id] = (title, text)

    return texts_dict



def parse_pages(pages):
    """
    Given iterable of paths to page files, return
    dictionary with 'P1', 'P2', etc as keys, and the
    root element of each page as values.
    """
    # Gives list members in order 0001, 0002 etc.
    pages = sorted(pages)
    page_roots = {}
    for i, page in enumerate(pages):
        tree = ET.parse(page)
        root = tree.getroot()
        page_roots[f'P{i+1}'] = root

    return page_roots



def process_block(block_strings):
    """
    Given xml String elements from text block, return whole block
    as single string.
    """
    words = []
    for s in block_strings:
        words.append(s.attrib['CONTENT'])
    total_string = ' '.join(words)

    return total_string


# TO DO: Split in two
def tokenise_and_stop(text):
    """
    Given text as list of text blocks, returned text tokenized and
    stopped.
    """
    total_string = ' '.join(text)
    tokens = TOKENIZER.tokenize(total_string.lower())
    stopped_tokens = [i for i in tokens if not i in STOPS]
    return stopped_tokens



def print_text(index, dataframe):
    """
    Given index, return string containing heading and body text.
    Assumes dataframe contains a 'Text' column containing lists of
    strings as entries as well as 'Title', 'Newspaper' columns
    containing strings and a 'Date' column containing integers.
    """
    newspaper = dataframe.loc[index, 'Newspaper']
    date = dataframe.loc[index, 'Date']
    title = dataframe.loc[index, 'Title']
    text_blocks = dataframe.loc[index, 'Text']
    wrapped_blocks = []
    for block in text_blocks:
        wrapped_string = textwrap.fill(block, width=80)
        wrapped_blocks.append(wrapped_string)
    text = '\n\n'.join(wrapped_blocks)
    article_string = f'{title}\n{newspaper} - {date}\n\n{text}'

    print(article_string)



def print_text_index_only(index, dataframe):
    """
    Given index, return string containing heading and body text.
    Assumes dataframe contains a 'Text' column containing lists of
    strings as entries as well as 'Title'. Works out newspaper and
    date from index.
    """
    newspaper = index[0:index.find('_')]
    date = index[index.find('_')+1:index.find('_')+9]
    title = dataframe.loc[index, 'Title']
    text_blocks = dataframe.loc[index, 'Text']
    wrapped_blocks = []
    for block in text_blocks:
        wrapped_string = textwrap.fill(block, width=80)
        wrapped_blocks.append(wrapped_string)
    text = '\n\n'.join(wrapped_blocks)
    article_string = f'{title}\n{newspaper} - {date}\n\n{text}'

    print(article_string)


def html_text(index, dataframe, boldface=None):
    """
    Given article code, return html formatted text
    containing both heading and body text. Optionally, boldface
    matches of the boldface regex expression.
    Assumes dataframe contains a 'Text' column containing lists of
    strings as entries as well as 'Title', 'Newspaper' columns
    containing strings and a 'Date' column containing integers.

    I only escape html characters in the title and text. Newspaper and
    data should not have any html in them. Leaving them unescaped
    increases the chance of finding any such errors.
    """
    newspaper = dataframe.loc[index, 'Newspaper']
    date = dataframe.loc[index, 'Date']
    title = html.escape(dataframe.loc[index, 'Title'])
    text_blocks = dataframe.loc[index, 'Text']
    text = ''
    for block in text_blocks:
        tagged_string = f'<p>{html.escape(block)}</p>'
        text += tagged_string

    if boldface:
        match = re.search(boldface, text)
        if match:
            text = re.sub(boldface, f'<b>{match.group(0)}</b>', text)

    article_string = f'<h3>{title}</h3><h4>{newspaper} - {date}</h4>{text}'

    return HTML(article_string)



def search_text(dataframe, re_string, lower=False):
    """
    Given dataframe with 'Text' column as described above, search for
    re string within 'Text' column content and return article codes
    containing the search string.

    This can be very slow. OK on starter pack dataset though.
    """
    article_codes = set()
    for row in dataframe.itertuples():
        for string in row.Text:

            if lower:
                string = string.lower()

            match = re.search(re_string, string)

            if match:
                article_codes.add(row.Index)

    return list(article_codes)



def blocks2string(text_blocks):
    """Given textblocks return blocks as single string."""
    return '\n'.join(text_blocks)



def interactive_text_search(dataframe, search_term):
    """
    Produce interactive display to inspect result of searching for a given
    regex pattern in the 'Text' column of the given dataframe.
    """
    search_indices = search_text(dataframe, search_term)
    print(f'Article matches: {len(search_indices)}')
    interact(
        html_text,
        index=search_indices,
        boldface=fixed(search_term),
        dataframe=fixed(dataframe)
    )



def log_dice_coocs(term, dtm, ttm, num_coocs):
    """Return num_coocs with log dice significance stat given search term
    document-term matrix and term-term matrix. Return as
    pandas series with terms as indices and significances as values..
    ttm and dtm are pandas dataframes."""
    all_term_occurrences = dtm.sum(axis=1)
    term_occurrences = all_term_occurrences[term]
    cooccurrences = ttm.loc[term]
    log_dice = np.log(2 * cooccurrences / (term_occurrences + all_term_occurrences))
    log_dice = log_dice.sort_values(ascending=False)[0:num_coocs]
    return log_dice



def mi_coocs(term, dtm, ttm, num_coocs):
    """Return num_coocs with mutual information sig score given search term
    document-term matrix and term-term matrix. Return as
    pandas series with terms as indices and significances as values..
    ttm and dtm are pandas dataframes."""
    num_documents = len(dtm.columns)
    all_term_occurrences = dtm.sum(axis=1)
    term_occurrences = all_term_occurrences[term]
    cooccurrences = ttm.loc[term]
    mi = np.log(num_documents * cooccurrences / (term_occurrences * all_term_occurrences))
    mi = mi.sort_values(ascending=False)[0:num_coocs]
    return mi



def network_dict(term, stat, dtm, ttm, num_coocs):
    """Produce network dataframe."""

    network = {}
    if stat == 'log dice':
        term_coocs = log_dice_coocs(term, dtm, ttm, num_coocs)
    elif stat == 'ml':
        term_coocs = mi_coocs(term, dtm, ttm, num_coocs)

    for item in term_coocs.iteritems():
        if item[0] != term:
            from_list = network.get('source', [])
            from_list.append(term)
            network['source'] = from_list
            to_list = network.get('target', [])
            to_list.append(item[0])
            network['target'] = to_list
            weight_list = network.get('weight', [])
            weight_list.append(item[1])
            network['weight'] = weight_list

        if stat == 'log dice':
            item_coocs = log_dice_coocs(item[0], dtm, ttm, num_coocs)
        elif stat == 'ml':
            item_coocs = mi_coocs(item[0], dtm, ttm, num_coocs)
        for sub_item in item_coocs.iteritems():
            if item[0] != sub_item[0]:
                from_list = network.get('source', [])
                from_list.append(item[0])
                network['source'] = from_list
                to_list = network.get('target', [])
                to_list.append(sub_item[0])
                network['target'] = to_list
                weight_list = network.get('weight', [])
                weight_list.append(sub_item[1])
                network['weight'] = weight_list

    return network



def network_dash(term, stat, dtm, ttm, num_coocs, sec_coocs):
    """Produce network dataframe formatted for Dash cytoscope."""

    if stat == 'log dice':
        term_coocs = log_dice_coocs(term, dtm, ttm, num_coocs)
    elif stat == 'mi':
        term_coocs = mi_coocs(term, dtm, ttm, num_coocs)

    nodes = []
    node_names = set([term])
    edges = []

    for item in term_coocs.iteritems():
        node_names.add(item[0])
        if item[0] != term:
            edges.append({'data': {
                'source': term,
                'target': item[0],
                'weight': item[1]}
                }
            )

        if stat == 'log dice':
            item_coocs = log_dice_coocs(item[0], dtm, ttm, sec_coocs)
        elif stat == 'mi':
            item_coocs = mi_coocs(item[0], dtm, ttm, sec_coocs)
        for sub_item in item_coocs.iteritems():
            node_names.add(sub_item[0])
            if item[0] != sub_item[0]:
                edges.append({'data': {
                    'source': item[0],
                    'target': sub_item[0],
                    'weight': sub_item[1]}
                    }
                )

    for name in node_names:
        nodes.append({'data': {
            'id': name,
            'label': name,
            'size': node_degree(name, edges)}
            }
        )

    network = nodes + edges

    return network



def node_degree(name, edges):
    """Helper for dash network. Returns degree of node given
    list of edges formatted for Dash cytoscape."""
    degree=0
    for edge in edges:
        if edge['data']['source'] == name or edge['data']['target'] == name:
            degree += 1
    return degree



def filter_propns(set_of_words):
    """
    Given set of proper nouns as detected by Spacy, strip whitespace, and
    return set of words of length greater than two and which start
    with a capitol letter followed by lower case letters.
    """
    filtered_set = set()
    for word in set_of_words:
        word = word.strip()
        match = bool(re.match('[A-Z][a-z]+', word))
        word_wanted = len(word) > 2 and match
        if word_wanted:
            filtered_set.add(word)

    return filtered_set



def filter_entities(set_of_strings):
    """
    Given set of named entities as detected by Spacy, strip whitespace,
    make lower case and return set of words of length greater than two and
    which do not contain any punctuation characters (excluding apostrophes).
    """
    filtered_set = set()
    for entity in set_of_strings:
        entity = entity.strip().lower()
        match = bool(re.match("[a-z ']+$", entity))
        entity_wanted = len(entity) > 2 and match
        if entity_wanted:
            filtered_set.add(entity)

    return filtered_set



def classify_text():

    readable = phil = phil_type = genre_type = nz = notes = None

    readable_in = input('Long readable portions? (y if readable)> ')
    if readable_in == 'y':
        readable = True
    else:
        readable = False

    if readable == True:
        phil_in = input('Philosophy? (y if so)> ')
        if phil_in == 'y':
            phil = True
        else:
            phil = False

    if readable == True and phil == True:
        phil_type_in = input('Ethics/Epistemology-Metaphysics/Religion-Science/Other? (e/m/r/o)> ')
        if phil_type_in in ['e', 'm', 'r', 'o']:
            phil_type = phil_type_in
        else:
            phil_type = 'input error'

        genre_type_in = input('Public event/letter/review/first order? (p/l/r/f)> ')
        if genre_type_in in ['p', 'l', 'f', 'r']:
            genre_type = genre_type_in
        else:
            genre_type = 'input error'

        nz_in = input('NZ or non-NZ (author)? (y/n/?)')
        if nz_in == 'y':
            nz = True
        elif nz_in == 'n':
            nz = False

    notes = input('Notes? >')

    return (readable, phil, phil_type, genre_type, nz, notes)



def classify_text_v2():
    """Implement second version of classification scheme. See
    'Relabelling.ipynb'."""

    readable = phil = phil_type = genre_type = nz = notes = None

    readable_in = input('Readable? (y/n)> ')
    if readable_in == 'y':
        readable = True
    else:
        readable = False

    if readable == True:
        phil_in = input('Philosophy? (y/n)> ')
        if phil_in == 'y':
            phil = True
        else:
            phil = False

    if readable == True and phil == True:
        phil_type_in = input('Ethics-Politics/Religion-Science/Other? (e/r/o)> ')
        if phil_type_in in ['e', 'r', 'o']:
            phil_type = phil_type_in
        else:
            phil_type = 'input error' #Correct later, I'm not having nested while loops.

    if readable == True:
        genre_type_in = input('Public event/letter/review/first order? (p/l/r/f)> ')
        if genre_type_in in ['p', 'l', 'f', 'r']:
            genre_type = genre_type_in
        else:
            genre_type = 'input error'

        nz_in = input('NZ or non-NZ (author)? (y/n/?)')
        if nz_in == 'y':
            nz = True
        elif nz_in == 'n':
            nz = False

    notes = input('Notes? >')

    return (readable, phil, phil_type, genre_type, nz, notes)



def add_title_and_date(df):
    """Add 'Newspaper' and 'Date' column to dataframe with
    'Text' and 'Tokenised' columns. Rearrange dataframe to
    have ['Newspaper', 'Date', 'Title', 'Text', 'Tokenised']
    order."""
    df['Newspaper'] = df.index.map(lambda x: x[0:x.find('_')])
    df['Date'] = df.index.map(lambda x: x[x.find('_')+1:x.find('_')+9])


def remove_duplicates(dataframe):
    """Given dataframe with duplicate indices, remove duplicates."""
    dataframe = dataframe[~dataframe.index.duplicated(keep='first')]
    return dataframe
