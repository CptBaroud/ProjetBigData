from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client['DataProject']
collection_stamped = db['vehicules_stamped']

date = list()
heure = list()

for date in collection_stamped.find({}, {'date': 1}):
    temp = datetime.datetime.strptime(date['date'], "%d/%m/%Y %Hh%Mm")
    date.append(temp.date())
    heure.append(temp.time())

print(date)
print(heure)
