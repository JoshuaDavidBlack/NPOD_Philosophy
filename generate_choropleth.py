"""
DATA601

Generate choropleth for Rel corpus articles as proportion of total articles by region.
"""
import pickle

import pandas as pd

import NL_helpers

DATASET_PATH = '/home/joshua/hdd/Datasets/papers-past/'

with open('dictionaries/codes2names.pickle', 'rb') as fin:
    codes2names = pickle.load(fin)

# Generate the data.
names2codes = {}
for k, v in codes2names.items():
    names2codes[v] = k

input_string = """Albertland Gazette 	Auckland
Auckland Chronicle and New Zealand Colonist 	Auckland
Auckland Star 	Auckland
Auckland Times 	Auckland
Daily Southern Cross 	Auckland
New Zealand Herald 	Auckland
New Zealand Herald and Auckland Gazette 	Auckland
New Zealander 	Auckland
Observer 	Auckland
Bay of Plenty Times 	Bay of Plenty
Hot Lakes Chronicle 	Bay of Plenty
Akaroa Mail and Banks Peninsula Advertiser 	Canterbury
Ashburton Guardian 	Canterbury
Ashburton Herald 	Canterbury
Ellesmere Guardian 	Canterbury
Globe 	Canterbury
Lyttelton Times 	Canterbury
Oxford Observer 	Canterbury
Press 	Canterbury
South Canterbury Times 	Canterbury
Star (Christchurch) 	Canterbury
Temuka Leader 	Canterbury
Timaru Herald 	Canterbury
Waimate Daily Advertiser 	Canterbury
Matariki 	Gisborne
Poverty Bay Herald 	Gisborne
Takitimu 	Gisborne
Bush Advocate 	Hawke's Bay
Daily Telegraph 	Hawke's Bay
Hastings Standard 	Hawke's Bay
Hawke's Bay Herald 	Hawke's Bay
Hawke's Bay Times 	Hawke's Bay
Hawke's Bay Weekly Times 	Hawke's Bay
Waipawa Mail 	Hawke's Bay
Feilding Star 	Manawatu-Wanganui
Manawatu Herald 	Manawatu-Wanganui
Manawatu Standard 	Manawatu-Wanganui
Manawatu Times 	Manawatu-Wanganui
Pahiatua Herald 	Manawatu-Wanganui
Wanganui Chronicle 	Manawatu-Wanganui
Wanganui Herald 	Manawatu-Wanganui
Woodville Examiner 	Manawatu-Wanganui
Marlborough Daily Times 	Marlborough
Marlborough Express 	Marlborough
Marlborough Press 	Marlborough
Pelorus Guardian and Miners' Advocate. 	Marlborough
Anglo-Maori Warder 	National
Aotearoa : he Nupepa ma nga Tangata Maori 	National
Haeata 	National
Hiiringa i te Whitu 	National
Hokioi o Nui-Tireni, e rere atuna 	National
Huia Tangata Kotahi 	National
Jubilee : Te Tiupiri 	National
Kahiti Tuturu mo Aotearoa, me te Waipounamu 	National
Korimako 	National
Maori Messenger : Te Karere Maori 	National
Pihoihoi Mokemoke i Runga i te Tuanui 	National
Saturday Advertiser 	National
Waka Maori 	National
Wananga 	National
Whetu o te Tau 	National
Colonist 	Nelson
Golden Bay Argus 	Nelson
Nelson Evening Mail 	Nelson
Nelson Examiner and New Zealand Chronicle 	Nelson
New Zealand Advertiser and Bay of Islands Gazette 	Northland
Northern Advocate 	Northland
Bruce Herald 	Otago
Clutha Leader 	Otago
Cromwell Argus 	Otago
Dunstan Times 	Otago
Evening Star 	Otago
Lake County Press 	Otago
Lake Wakatip Mail 	Otago
Mataura Ensign 	Otago
Mount Ida Chronicle 	Otago
Mt Benger Mail 	Otago
North Otago Times 	Otago
Oamaru Mail 	Otago
Otago Daily Times 	Otago
Otago Witness 	Otago
Southern Cross 	Otago
Southland Times 	Otago
Tuapeka Times 	Otago
Western Star 	Otago
Samoa Times and South Sea Advertiser 	Samoa
Samoa Times and South Sea Gazette 	Samoa
Samoa Weekly Herald 	Samoa
Hawera & Normanby Star 	Taranaki
Opunake Times 	Taranaki
Patea Mail 	Taranaki
Taranaki Herald 	Taranaki
Ohinemuri Gazette 	Waikato
Paki o Matariki 	Waikato
Te Aroha News 	Waikato
Thames Advertiser 	Waikato
Thames Guardian and Mining Record 	Waikato
Thames Star 	Waikato
Waikato Argus 	Waikato
Waikato Times 	Waikato
Evening Post 	Wellington
Karere o Poneke 	Wellington
New Zealand Colonist and Port Nicholson Advertiser 	Wellington
New Zealand Gazette and Wellington Spectator 	Wellington
New Zealand Mail 	Wellington
New Zealand Spectator and Cook's Strait Guardian 	Wellington
New Zealand Times 	Wellington
Puke ki Hikurangi 	Wellington
Victoria Times 	Wellington
Wairarapa Daily Times 	Wellington
Wairarapa Standard 	Wellington
Wellington Independent 	Wellington
Charleston Argus 	West Coast
Grey River Argus 	West Coast
Inangahua Times 	West Coast
Kumara Times 	West Coast
Lyell Times and Central Buller Gazette 	West Coast
West Coast Times 	West Coast
Westport Times 	West Coast"""

code2region = {}
pairs = [pair_string.split(' \t') for pair_string in input_string.split('\n')]

for pair in pairs:
    newspaper = pair[0]
    region = pair[1]
    try:
        code = names2codes[newspaper]
        code2region[code] = region
    except KeyError:
        pass

rel_df = pd.read_pickle('pickles/rel_v2_philoso_df.tar.gz')

region2relcount = {}
counts_by_newspaper = rel_df['Newspaper'].value_counts()
for (code, count) in counts_by_newspaper.iteritems():
    region = code2region[code]
    current_count = region2relcount.get(region, 0)
    new_count = current_count + count
    region2relcount[region] = new_count

region2totalcount = {}
for i in range(9):
    print(i)
    df = pd.read_pickle(DATASET_PATH+f'corpus_df_{i}.tar.gz')
    NL_helpers.add_title_and_date(df)
    counts_by_newspaper = df['Newspaper'].value_counts()
    for (code, count) in counts_by_newspaper.iteritems():
        region = code2region[code]
        current_count = region2totalcount.get(region, 0)
        new_count = current_count + count
        region2totalcount[region] = new_count
    del df

region2prop = {}
for region, rel_count in region2relcount.items():
    region2prop[region] = rel_count/region2totalcount[region]


region2prop

props_df = pd.DataFrame.from_dict(
    data=region2prop,
    orient='index',
    columns = ['prop']
)

# Using map as efficiency no issue with such a small amount of data
props_df['prop'] = props_df['prop'].map(lambda x: x * 1000)
props_df['region'] = props_df.index.map(lambda x: f'{x} Region')
props_df

props_df.to_csv('csv/props.csv')

import json
with open('choropleth/nz_regions.geojson') as infile:
    nz_regions = json.load(infile)

import plotly.express as px

nz_regions

import branca
import folium


for feature in nz_regions['features']:
    try:
        region = feature['properties']['REGC2016_N'][:-7]
        feature['properties']['proportion'] = region2prop[region]
    except KeyError:
        feature['properties']['proportion'] = None



m = folium.Map(
    location=['-41.280710', '175.070684'],
    tiles=None,
    zoom_start=5,
    zoom_control=False,
)

# Colorize the region using a color scale
colorscale = branca.colormap.linear.Reds_09.scale(0, 0.003)
colorscale.caption="Proportion of Newspaper Articles Concerning Religion and Science"
colorscale.add_to(m)

def set_colour(prop):
    if prop is None:
        colour = 'black'
    else:
        colour = colorscale(prop)
    return colour

def style_function(feature):
    prop = feature['properties']['proportion']
    return {
        'fillOpacity': 0.5,
        'fillColor': set_colour(prop),
        'weight': 1,
        'color': 'black',
    }


# Add DHB geojson to map
folium.GeoJson(
    nz_regions,
    name='geojson',
    style_function=style_function
).add_to(m)

m.save('rel_sci_choropleth.html')
