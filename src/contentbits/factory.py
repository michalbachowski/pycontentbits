#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
from contentbits.types import Collection, Item


class CollectionFactory(object):

    def __init__(self, collection=None, item=None):
        if collection is None:
            collection = Collection
        if item is None:
            item = Item
        self._collection = collection
        self._item = item

    def discover(self, input):
        # from dictionary
        if hasattr(input, 'items'):
            return self.from_dict(input)
        # list
        if hasattr(input, 'append'):
            return self.from_list(input)
        # from iterator with tuples
        try:
            tmp = next(input)
            id, data = tmp
        except TypeError:
            func = self.from_iterator
        else:
            func = self.from_iterator_with_tuples
        finally:
            input = itertools.chain([tmp], input)
        return func(input)

    def from_dict(self, input):
        return self.from_iterator_with_tuples(input.items())

    def from_list(self, input):
        return self.from_iterator(list(input))

    def from_iterator(self, input):
        return self.from_iterator_with_tuples(zip(itertools.repeat(None),
                input))

    def from_iterator_with_tuples(self, input):
        c = self._collection()
        for (id, data) in input:
            c.append(self._item(data, id))
        return c
