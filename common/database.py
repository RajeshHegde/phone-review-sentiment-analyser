'''
Created on 24 Apr 2016

@author: RAJESH
'''

import logging
from pymongo import MongoClient

class Database:
    def __init__(self):
        client = MongoClient()
        self.db = client.reviews