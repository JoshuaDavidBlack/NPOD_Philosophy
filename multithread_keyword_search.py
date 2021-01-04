import re
import tarfile
import os
import glob
import time
from multiprocessing import Pool

import pandas as pd
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

import NL_helpers

TOKENIZER = RegexpTokenizer(r"\w[\w\']+\w")
STOPS = set(stopwords.words())

NS = {'mets':'http://www.loc.gov/METS/'}

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'

TARBALLS = glob.glob(DATASET_PATH + '*/*.tar.gz')
FILTER_STRING = 'philoso*'


def process_tarball(filepath):
    """
    Given path to tarball, open and return dataframe containing article
    items from tarball.
    """
    newspaper_year = tarfile.open(filepath)
    files = newspaper_year.getmembers()
    issues = collect_issues(files)
    articles = collect_articles(issues, newspaper_year)

    return articles



def collect_issues(files):
    """
    Given list of files in tarball, return a dictionary keyed
    by the issue code with list of xml files of form [0001.xml, ..., mets.xml]
    as values.
    """
    issues = {}
    issue_code = ''
    for file in files:
        match = re.search("[A-Z]*_\d{8}$", file.name)
        if match:
            issue_code = match.group(0)
        if file.name.endswith('.xml'):
            xml_list = issues.get(issue_code, [])
            xml_list.append(file)
            issues[issue_code] = xml_list
    return issues


def collect_articles(issues, newspaper_year):
    """Given list of issues and corresponding xml files,
    return dictionary containing article codes as keys and
    texts (as list of strings for each block as values."""
    articles = {}
    i = 0
    for issue_code, issue_files in issues.items():
        mets_tarinfo = issue_files[-1]
        pages_tarinfo = issue_files[0:-1]
        article_codes = mets2codes_tar(mets_tarinfo, newspaper_year)
        all_articles = codes2texts_tar(article_codes, pages_tarinfo, newspaper_year, issue_code)
        articles = {**articles, **all_articles} # Merge dictionaries.
        i+=1

    return articles



def mets2codes_tar(mets_tarinfo, newspaper_year):
    """
    Given mets as tarinfo, return text block codes for articles
    contained in mets file. Edited for processing with tarfile
    object newspaper_year.

    Returns dictionary of article codes as keys,
    with a 2-tuple containing the article title
    and a list of corresponding text block codes as values.
    """
    with newspaper_year.extractfile(mets_tarinfo) as file:
        text = file.read()
    mets_root = ET.fromstring(text)
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
            try:
                area = block.find(".//mets:area", NS)
                block_id = area.attrib['BEGIN']
                block_ids.append(block_id)
            except AttributeError:
                print(f'Error in {newspaper_year}')
        art_dict[article_id] = (article_title, block_ids)

    return art_dict



def codes2texts_tar(article_codes, pages_tarinfo, newspaper_year, issue_code):
    """
    Given list of articles and their text block codes, and a list of
    the ALTO files for each page in the issue, return a dictionary
    with article codes as keys and a list of text blocks as
    strings as values.

    REWRITTEN FOR TARBALLS
    """

    page_roots = parse_pages_tar(pages_tarinfo, newspaper_year)

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
            block_as_string = NL_helpers.process_block(block_strings)
            text.append(block_as_string)
        issue_article_id = issue_code + '_' + article_id[7:]
        texts_dict[issue_article_id] = (title, text)

    return texts_dict



def parse_pages_tar(pages, newspaper_year):
    """
    Given iterable of paths to page files, return
    dictionary with 'P1', 'P2', etc as keys, and the
    root element of each page as values.

    REWITTEN FOR TARBALL APPROACH
    """
    # Gives list members in order 0001, 0002 etc.
    page_roots = {}
    for i, page in enumerate(pages):
        with newspaper_year.extractfile(page) as f:
            text = f.read()
        root = ET.fromstring(text)
        page_roots[f'P{i+1}'] = root

    return page_roots


def process_and_filter(path):
    """
    Return filtered dataframe of articles only containing the search term
    given a path to a tarball for a year of issues of a papers past
    newspaper.
    """
    print(f'Processing {path}')
    try:
        articles = process_tarball(path)
        dataframe = pd.DataFrame.from_dict(
            articles,
            orient='index',
            dtype = object,
            columns=['Title', 'Text']
            )
        filtered_dataframe = dataframe.loc[NL_helpers.search_text(dataframe, FILTER_STRING),]
    except:
        print(f'Problem with {path}')
        filtered_dataframe = None
    return filtered_dataframe

t0 = time.time()
# len(TARBALLS) # 1656 = 2^3*3^2*23
for sub_group in range(8):
    balls = TARBALLS[sub_group * 207: (sub_group+1)*207]
    num_balls = len(balls)
    dfs = {}
    j = 0
    if __name__ == '__main__':
        with Pool(processes=16) as pool:
            filtered_dfs = pool.imap(process_and_filter, balls)
            i = 0
            for filtered_df in filtered_dfs:
                print(f'{time.time()}: {i}/{num_balls}')
                try:
                    dfs[i] = filtered_df
                    i += 1
                except (ValueError, AttributeError):
                    j += 1
            df = pd.concat(dfs.values())
            df.to_pickle(DATASET_PATH + f'philoso_df_{sub_group}.tar.gz')
print(f'Time taken: {time.time() - t0}')
