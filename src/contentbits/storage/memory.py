#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import count
from contentbits.storage.abstract import Abstract
from contentbits.utils import as_deferred


class Memory(Abstract):
    """ Memory-based storage for collections """

    def __init__(self):
        """ Class initialization """
        self._collections = {}
        self._seq = count()

    def _get_idx(self, collection):
        """ Method genertes identificator for collection or item """
        # make sure that collection with given ID does not exist
        while True:
            idx = next(self._seq)
            if idx not in collection:
                return idx

    @as_deferred
    def read_collection(self, collection_id):
        return self._collections[collection_id]

    @as_deferred
    def create_collection(self, collection_id=None):
        # generate collection_id if not given
        if collection_id is None:
            collection_id = self._get_idx(self._collections)
        # make sure that we will not override existing collection
        if collection_id not in self._collections:
            self._collections[collection_id] = {}
        return collection_id

    @as_deferred
    def store_item(self, collection_id, data, item_id=None):
        if item_id is None:
            item_id = self._get_idx(self._collections[collection_id])
        self._collections[collection_id][item_id] = data
        return (collection_id, item_id)

    @as_deferred
    def remove_item(self, collection_id, item_id):
        del self._collections[collection_id][item_id]
        return (collection_id, item_id)

    @as_deferred
    def remove_collection(self, collection_id):
        del self._collections[collection_id]
        return collection_id
