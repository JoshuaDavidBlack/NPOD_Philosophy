def produce_sheets(model, corpus, corpus_df):

    # Putting this enumeration outside the loop means the model only
    # has to be run through once.
    corpus_enumerated = list(enumerate(model[corpus]))

    #### Primary and Secondary Topics for Each Document
    doc_topics_df = pd.DataFrame()
    for i, row in corpus_enumerated:
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the primary and secondary topic and contrib for each document
        prim_topic = int(row[0][0])
        prim_prop = round(row[0][1], 4)
        # Wrap in try as some documents will have only one topic.
        try:
            sec_topic = int(row[1][0])
            sec_prop = round(row[1][1], 4)
        except IndexError:
            sec_topic = sec_prop = None
        doc_topics_df = doc_topics_df.append(pd.Series([prim_topic,
            prim_prop, sec_topic, sec_prop]), ignore_index=True)
    doc_topics_df.columns = ['Primary Topic', 'Primary Perc',
                             'Secondary Topic', 'Secondary Perc']
    doc_topics_df.index = corpus.items_df.index
    doc_topics_df = doc_topics_df.convert_dtypes()

    #### Topics dataframe
    topic_df = pd.DataFrame()
    prim_counts = doc_topics_df['Primary Topic'].value_counts()
    sec_counts = doc_topics_df['Secondary Topic'].value_counts()
    prim_sizes = []
    sec_sizes = []
    rep_docs = []
    # Want a most characteristic document for each topic so must iterate
    # through all documents and all topics assigned to each topic as
    # some topics may not be either the primary or secondary topic
    # for any topic in the corpus.
    num_topics=model.num_topics

    for (topic_num, words) in model.show_topics(num_topics=num_topics):
        # Find most representative document
        topic_percs = []
        for i, row in corpus_enumerated:
            topic_perc = 0
            for topic in row:
                if topic[0] == topic_num:
                    topic_perc = topic[1]
            topic_percs.append(topic_perc)
        representative_doc_index = max(range(len(topic_percs)),
                                        key=lambda i: topic_percs[i])
        item_df_index = corpus_df.index[representative_doc_index]
        #rep_docs.append(item_df_index)

        # Collect keywords
        wp = model.show_topic(topic_num)
        topic_keywords = ", ".join([word for word, prop in wp])

        # Collect counts of docs for which topic is primary and secondary
        if topic_num in prim_counts.index:
            #prim_sizes.append(prim_counts.loc[topic_num])
            prim_size = prim_counts.loc[topic_num]
        else:
            prim_size = 0
            #prim_sizes.append(0)

        if topic_num in sec_counts.index:
            #sec_sizes.append(sec_counts.loc[topic_num])
            sec_size = sec_counts.loc[topic_num]
        else:
            #sec_sizes.append(0)
            sec_size = 0

        topic_df = topic_df.append(pd.Series([topic_num,
            topic_keywords, item_df_index, prim_size, sec_size]),
            ignore_index=True)
    topic_df = topic_df.convert_dtypes()
    topic_df.columns = ['Topic', 'Keywords', 'Representative Document',
        'Primary Size', 'Secondary Size']

    enriched_items_df = corpus_df.join(doc_topics_df)


    # Collect names of rep documents
    doc_names = []
    journal_names = []
    years = []
    for i, row in topic_df.iterrows():
        item_index = row[2]
        title, journal, year = tuple((corpus.items_df.loc[item_index,
                ['Title', 'Journal ID', 'Year']]))
        doc_names.append(title)
        journal_names.append(journal)
        years.append(year)
    enriched_topic_df = topic_df

    enriched_topic_df['Title'] = doc_names
    enriched_topic_df['Journal ID'] = journal_names
    enriched_topic_df['Year'] = years
    cols = ['Topic', 'Keywords', 'Representative Document',
            'Title', 'Journal ID', 'Year',  'Primary Size',
                   'Secondary Size']
    enriched_topic_df = enriched_topic_df[cols]

    enriched_topic_df.to_csv('model_sheets/'+prefix+'topics_enriched.csv')
    topic_df.to_csv('model_sheets/'+prefix+'topics.csv')
    enriched_items_df.to_csv('model_sheets/'+prefix+'enriched_items.csv')
#save em all.
