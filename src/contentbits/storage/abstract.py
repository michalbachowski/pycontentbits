#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Abstract(object):

    def read_collection(self, collection_id):
        raise NotImplementedError()

    def create_collection(self, collection_id=None):
        raise NotImplementedError()

    def store_item(self, collection_id, data, item_id=None):
        raise NotImplementedError()

    def remove_item(self, collection_id, item_id):
        raise NotImplementedError()

    def remove_collection(self, collection_id):
        raise NotImplementedError()
