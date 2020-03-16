
from pymongo import MongoClient
from key import auth


class Mongo:
    def __init__(self):
        self.client = MongoClient(
            f'mongodb+srv://ashvin14:{auth.mongo_atlas_password()}@financial-data-engg01-ktmp7.mongodb.net/test?retryWrites=true&w=majority')

    def connect_to_database(self, url='financial_data'):
        try:
            print('connected to database!')
            return self.client.get_database(url)
        except:
            print("Oops! Couldn't connect to database please check if database name was correct or not, else check connection")
