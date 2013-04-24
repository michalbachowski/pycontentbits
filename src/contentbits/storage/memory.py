#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import count
from contentbits.storage.abstract import Abstract


class Memory(Abstract):

    def __init__(self):
        self._collections = {}
        self._seq = count()

    def _get_idx(self):
        return next(self._seq)

    def read_collection(self, collection_id):
        return self._collections[collection_id]

    def create_collection(self, collection_id=None):
        if collection_id is None:
            collection_id = self._get_idx()
        if collection_id not in self._collections:
            self._collections[collection_id] = {}
        return collection_id

    def store_item(self, collection_id, data, item_id=None):
        if item_id is None:
            item_id = self._get_idx()
        self._collections[collection_id][item_id] = data
        return item_id

    def remove_item(self, collection_id, item_id):
        del self._collections[collection_id][item_id]
        return self

    def remove_collection(self, collection_id):
        del self._collections[collection_id]
        return self
