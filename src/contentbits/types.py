#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Collection(object):

    def __init__(self, id=None):
        self._id = None
        self._items = []
        self.id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = str(id)

    def append(self, item):
        self._items.append(item)
        return self

    def __str__(self):
        return self.id

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items

    def __eq__(self, other):
        return self.id == str(other)

    def __delitem__(self, item):
        self._items.remove(str(item))


class Item(object):

    def __init__(self, data, id=None):
        self._data = data
        self._id = None
        self.id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = str(id)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def __eq__(self, other):
        return self.id == str(other)

    def __str__(self):
        return self.id
