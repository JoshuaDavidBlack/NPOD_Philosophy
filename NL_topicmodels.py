from nltk.corpus import brown, stopwords
from nltk.tokenize import RegexpTokenizer
from gensim import corpora
import pandas as pd

class NL_corpus():
    """
    Corpus class for use with gensim for topic modelling.

    Input: 1) pandas dataframe containing 'Tokenised' column with
    tokenised texts for each article.
        2) Dictionary for use with gensim.

    Main benefit is use of iterator method.
    """

    def __init__(self, corpus_df, dictionary):
        self.items = corpus_df
        self.dictionary = dictionary
        self.generate_bow()

    def __iter__(self):
        for bag in self.items['BOW']:
            yield bag

    def generate_bow(self):
        """
        Generates bag of words representation of tokenised text and adds
        it to item dataframe as column 'BOW'.
        """
        bags = {}
        for index, value in self.items.iterrows():
            tokenised = value[4]
            bags[index] = [self.dictionary.doc2bow(tokenised)]
        bags_df = pd.DataFrame.from_dict(
            bags,
            orient='index',
            dtype = object,
            columns=['BOW']
            )
        self.items = self.items.join(bags_df)

    def __len__(self):
        """Returns number of corpus items."""
        return len(self.items)




def topics_and_keywords(model):
    """
    Given model, return dictionary of topics and keywords.
    """
    topic_kws = {}
    num_topics = model.num_topics
    for (topic_num, words) in model.show_topics(num_topics=num_topics):
        wp = model.show_topic(topic_num)
        topic_keywords = ", ".join([word for word, prop in wp])
        topic_kws[topic_num] = words
    return topic_kws



# This seems like far too many for loops!
def topic_proportions(items_df, num_topics):
    """
    Given an items dataframe with a 'Modelled' column and the total number
    of topics, return a copy of the corpus items dataframe augmented with
    scores for each of the topics in the model in individual columns.
    """
    topic_props = {}
    for model_output in items_df['Modelled']:
        # Create dictionary to store proportions of each topic. Initially
        # filled with 0's
        item_topic_props = {}
        for i in range(num_topics):
            item_topic_props[i] = 0

        # Take topic proportions for each topic from output and store
        # in dictionary
        for tuple in model_output:
            topic_num = tuple[0]
            topic_prop = tuple[1]
            item_topic_props[topic_num] = topic_prop

        # add to collection for all docuemnts.
        for k, v in item_topic_props.items():
            current_value = topic_props.get(k, [])
            topic_props[k] = current_value.append(v)

    for k, v in topic_props.items():
        items_df[k] = v

    return items_df
