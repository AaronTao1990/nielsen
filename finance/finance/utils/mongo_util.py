# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class MongoUtil(object):
    '''util to manage mongo connection and mongo opperations'''

    def __init__(self, host, db, coll):
        conn = MongoClient(host)
        self.db = conn[db]
        self.coll = self.db[coll]

    def find_all(self, query, limit=None):
        if limit:
            for item in self.coll.find(query).limit(limit):
                yield item
        else:
            for item in self.coll.find(query):
                yield item

    def count(self, query):
        return self.coll.find(query).count()

    def find_one(self, query):
        return self.coll.find_one(query)

    def save(self, item):
        self.coll.save(item)

    def insert(self, item):
        try:
            self.coll.insert(item)
        except DuplicateKeyError:
            return False
        return True

    def exists(self, query):
        for item in self.coll.find(query):
            return True
        return False

    def remove(self, query):
        self.coll.remove(query)

