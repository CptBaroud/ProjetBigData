from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client['DataProject']
collection_traffic = db['vehicules']

for trafic in collection_traffic.find():
    h = round(trafic['num_periode'] / 60)
    m = trafic['num_periode'] % 60
    j = trafic['num_jour'] + 1

    db['vehicules_stamped'].insert_one({'num_arete': trafic['num_arete'], 'date': datetime.datetime(2020, 1, j, h, m).strftime("%d/%m/%Y %Hh%Mm"),
                                                    'nb_vehicules': trafic['nb_vehicules']})
