#!/usr/bin/env python
# -*- coding: utf-8 -*-
from contentbits.factory import CollectionFactory


class Manager(object):

    def __init__(self, storage=None, collection_factory=None):
        self._storage = None
        self._collection_factory = None
        self.set_storage(storage)
        if collection_factory is None:
            collection_factory = CollectionFactory()
        self.set_collection_factory(collection_factory)

    def set_storage(self, storage):
        self._storage = storage
        return self

    def set_collection_factory(self, factory):
        self._collection_factory = factory
        return self

    def save_collection(self, collection):
        # read collection
        try:
            old_collection = self._storage.read_collection(collection.id)
        except KeyError:
            old_collection = {}
            collection.id = self._storage.create_collection(collection.id)
        old_collection = self._collection_factory.discover(old_collection)
        # add new items
        for item in collection:
            item.id = self.add_item_to_collection(collection.id, item)
            try:
                del old_collection[item]
            except ValueError:
                pass
        # remove old items
        for item in old_collection:
            self.remove_item_from_collection(collection.id, item.id)
        return collection.id

    def read_collection(self, collection_id):
        try:
            collection = self._storage.read_collection(collection_id)
        except KeyError:
            collection = {}
        c = self._collection_factory.discover(collection)
        c.id = collection_id
        return c

    def remove_collection(self, collection_id):
        self._storage.remove_collection(collection_id)
        return self

    def remove_item_from_collection(self, collection_id, item_id):
        self._storage.remove_item(collection_id, item_id)
        return self

    def add_item_to_collection(self, collection_id, item):
        return self._storage.store_item(collection_id, item.data, item.id)
