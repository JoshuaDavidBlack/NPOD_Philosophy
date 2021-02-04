import os
import pickle

os.chdir('/home/joshua/Documents/Academic/MADS/DATA601/')

with open('NLNZ_newspaperData.csv', 'r') as file:
    corpus_csv = file.readlines()

codes2names = {}
for line in corpus_csv[1:]:
    entries = line.split(',')
    codes2names[entries[0][0:entries[0].find('_')]] = entries[1]

codes2names

with open('dictionaries/codes2names.pickle', 'wb') as fout:
    pickle.dump(codes2names, fout)

codes2names_web = {}
for line in corpus_csv[1:]:
    entries = line.split(',')
    codes2names_web[entries[0][0:entries[0].find('_')]] = (
        entries[1]
        .lower()
        .replace('& ', '')
        .replace(' ', '-')
        .replace("'", '-')
    )
codes2names_web

with open('dictionaries/codes2names_web.pickle', 'wb') as fout:
    pickle.dump(codes2names_web, fout)

test_string = 'New Zealand Colonist and Port Nicholson Advertiser'
test_string = test_string.lower().replace(' ', '-')
test_string
