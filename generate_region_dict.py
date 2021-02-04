import pickle

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
