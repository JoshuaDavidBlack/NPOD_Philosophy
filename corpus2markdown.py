"""
Given corpus prefix, output the full corpus formatted as markdown documents at
a given output folder.
"""
import pickle
import os
import errno

import pandas as pd

CORPUS_PREFIX = 'nb2_v2'
OUTPUT_PATH = '/home/joshua/hdd/Datasets/nb2/'

with open('dictionaries/codes2names_web.pickle', 'rb') as infile:
    CODES2NAMES_WEB = pickle.load(infile)
with open('dictionaries/codes2names.pickle', 'rb') as infile:
    CODES2NAMES = pickle.load(infile)

def escape_markdown(string):
    """Escape characters which have functions in markdown strings.
    Return escaped string."""

    markdown_escape_chars = r"\`*_{}[]<>()#+-.!|"
    for escape_char in markdown_escape_chars:
        string = string.replace(escape_char, "\\"+escape_char)

    return string



def text_as_markdown(index, dataframe, boldface=None):
    """Render article corresponding to index in dataframe as markdown
    string. Any matches for boldface are rendered in bold.
    """

    date = index[index.find('_')+1:index.find('_')+9]
    newspaper = index[0:index.find('_')]

    title = (dataframe.loc[index, 'Title'])
    title = escape_markdown(title)

    web_prefix = "https://paperspast.natlib.govt.nz/newspapers/"
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    web_address = f"{web_prefix}{CODES2NAMES_WEB[newspaper]}/{year}/{month}/{day}"

    text_blocks = dataframe.loc[index, 'Text']
    text = ''
    for block in text_blocks:
        paragraph = escape_markdown(block)
        text += paragraph + '\n\n'

    if boldface:
        match = re.search(boldface, text)
        if match:
            text = re.sub(boldface, f'***{match.group(0)}***', text)

    markdown_text = f"""## {title}

*{CODES2NAMES[newspaper]}*

{day}/{month}/{year}

[View issue on Papers Past]({web_address})

{text}
"""

    return markdown_text


def main():
    df = pd.read_pickle(f'pickles/{CORPUS_PREFIX}_philoso_df.tar.gz')
    for i in df.index:
        formatted = text_as_markdown(i, df)
        newspaper = df.loc[i]['Newspaper']

        # create required directories
        # see: https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
        filename = f'{OUTPUT_PATH}{newspaper}/{i}.md'
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(filename, 'w') as outfile:
            outfile.write(formatted)

main()
