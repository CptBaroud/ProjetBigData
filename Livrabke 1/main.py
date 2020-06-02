from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client['DataProject']
collection_traffic = db['vehicules']

if db['vehicules_stamped'].count() <= 0:
    for trafic in collection_traffic.find():
        h = round(trafic['num_periode'] / 60)
        m = trafic['num_periode'] % 60
        j = trafic['num_jour'] + 1

        if trafic['plage_horaire'] == 'm':
            db['vehicules_stamped'].insert_one({'num_arete': trafic['num_arete'],
                                                'date': datetime.datetime(2020, 1, j, 7+h, m).strftime("%d/%m/%Y %Hh%Mm"),
                                                'nb_vehicules': trafic['nb_vehicules']})
        else:
            db['vehicules_stamped'].insert_one({'num_arete': trafic['num_arete'],
                                                'date': datetime.datetime(2020, 1, j, 17+h, m).strftime("%d/%m/%Y %Hh%Mm"),
                                                'nb_vehicules': trafic['nb_vehicules']})
else:
    print('La base est déjà remplie')
