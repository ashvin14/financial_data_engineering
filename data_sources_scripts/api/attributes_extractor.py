#! /usr/bin/env python3
import sys
from Symbols_extractor import symbols
from api import Batch
from key import auth
from mongo_connection import Mongo

db = Mongo().connect_to_database()
financial_data = db.ods_values


def response_of_symbol(s):
    return Batch(s).quote()[s]


for s in symbols:
    try:
        financial_data.insert_one(response_of_symbol(s))
    except:
        print("couldn't insert data for Symbol: "+s)
