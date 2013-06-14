#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
import six
from promise import Deferred
from contentbits.factory import CollectionFactory
from contentbits.utils import inject_deferred_return_promise


class Manager(object):

    class CollectionSaveHelper(six.Iterator):

        def __init__(self, manager, new_collection):
            self.deferred = Deferred()
            self._manager = manager
            self.new_collection = new_collection
            self.old_collection = None
            self.items = iter(new_collection)

        def __next__(self):
            return next(self.items)

        def save(self):
            # read current state of collection (it`s items)
            # if collection exists - go to next step
            # otherwise create new collection
            self._manager.storage.read_collection(self.new_collection.id)\
                    .done(partial(self._collection_found))\
                    .fail(partial(self._collection_not_found))

            return self.deferred.promise()

        def _collection_found(self, old_collection):
            self.old_collection = self._manager.collection_factory.discover(old_collection)
            self._add_items()

        def _collection_not_found(self, exception):
            self._manager.storage.create_collection(self.new_collection.id)\
                    .done(partial(self._collection_created))\
                    .fail(self.deferred.reject)

        def _collection_created(self, collection_id):
            self.new_collection.id = collection_id
            # lie that old collection was just empty
            self._collection_found([])

        def _add_items(self):
            try:
                self._manager.add_item_to_collection(self.new_collection,
                        next(self)).done(self._item_added)\
                        .fail(self.deferred.reject)
            except StopIteration:
                self._del_items()

        def _item_added(self, item_id):
            try:
                del self.old_collection[item_id]
            except:
                pass
            self._add_items()

        def _del_items(self, deleted_item_id=None):
            try:
                self._manager.remove_item_from_collection(
                        self.new_collection.id, next(self.old_collection).id)\
                        .done(partial(self._del_items))\
                        .fail(self.deferred.reject)
            except StopIteration:
                self.deferred.resolve(self.new_collection.id)

    def __init__(self, storage=None, collection_factory=None):
        self._storage = None
        self._collection_factory = None
        self.set_storage(storage)
        if collection_factory is None:
            collection_factory = CollectionFactory()
        self.set_collection_factory(collection_factory)

    @property
    def storage(self):
        return self._storage

    def set_storage(self, storage):
        self._storage = storage
        return self

    def set_collection_factory(self, factory):
        self._collection_factory = factory
        return self

    @property
    def collection_factory(self):
        return self._collection_factory

    def save_collection(self, collection):
        return Manager.CollectionSaveHelper(self, collection).save()

    def read_collection(self, collection_id):
        deferred = Deferred()

        def _done(collection):
            c = self._collection_factory.discover(collection)
            c.id = collection_id
            deferred.resolve(c)

        self._storage.read_collection(collection_id)\
                .done(_done).fail(deferred.reject)
        return deferred.promise()

    def remove_collection(self, collection_id):
        return self._storage.remove_collection(collection_id)

    def remove_item_from_collection(self, collection_id, item_id):
        return self._storage.remove_item(collection_id, item_id)

    @inject_deferred_return_promise
    def add_item_to_collection(self, deferred, collection, item):
        self._storage.store_item(collection.id, item.data, item.id)\
                .done(partial(self._item_added_to_collection, deferred,
                        collection, item))\
                .fail(deferred.reject)

    def _item_added_to_collection(self, deferred, collection, item, item_id):
        item.id = item_id
        collection.append(item)
        deferred.resolve(collection, item)
