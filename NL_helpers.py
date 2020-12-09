"""
NL_helpers.py
Joshua Black
black.joshuda@gmail.com

Contains helper functions for usings NLOD dataset.
"""

import xml.etree.ElementTree as ET
import glob
import os.path
import pandas as pd
import ast
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

TOKENIZER = RegexpTokenizer(r"\w[\w\']+\w")
STOPS = set(stopwords.words())

NS = {'mets':'http://www.loc.gov/METS/'}

def issue2articles(filepath):
    """Given string containing filepath to issue, return plain text
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
    # Gives list memebers in order 0001, 0002 etc.
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


def tokenise_and_stop(text):
    """Given text as list of text blocks, returned text tokenized and
    stopped.
    """
    total_string = ' '.join(text)
    tokens = TOKENIZER.tokenize(total_string.lower())
    stopped_tokens = [i for i in tokens if not i in STOPS]
    return stopped_tokens
