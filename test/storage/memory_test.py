#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

# hack for loading modules
import _path
_path.fix(2)


##
# content bits modules
#
from contentbits.storage.memory import Memory


class MemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.collection = Memory()

    def test_read_collection_raises_key_error_for_non_existing_collection(self):
        err = False
        try:
            self.collection.read_collection('foo')
        except KeyError:
            err = True
        self.assertTrue(err)

    def test_create_collection_returns_collection_id(self):
        self.assertIsNotNone(self.collection.create_collection())

    def test_create_collection_does_nothing_when_collection_Exists(self):
        idx = self.collection.create_collection()
        idxb = self.collection.store_item(idx, 'b')
        self.assertEqual(self.collection.create_collection(idx), idx)
        c = self.collection.read_collection(idx)
        self.assertTrue(idxb in c)
        self.assertEqual(c[idxb], 'b')

    def test_read_collection_returns_dict_for_existing_collection(self):
        idx = self.collection.create_collection()
        self.assertEqual(self.collection.read_collection(idx), {})

    def test_read_collection_returns_item_added_to_collection(self):
        idx = self.collection.create_collection()
        idxa = self.collection.store_item(idx, data='a')
        idxb = self.collection.store_item(idx, data='b')
        c = self.collection.read_collection(idx)
        self.assertTrue(idxa in c)
        self.assertTrue(idxb in c)
        self.assertEqual(c[idxa], 'a')
        self.assertEqual(c[idxb], 'b')

    def test_store_item_expects_collection_to_exist(self):
        err = False
        try:
            self.collection.store_item('foo', None)
        except KeyError:
            err = True
        self.assertTrue(err)

    def test_store_item_returns_item_id(self):
        idx = self.collection.create_collection()
        self.assertIsNotNone(self.collection.store_item(idx, None))

    def test_remove_item_expects_collection_to_exist(self):
        err = False
        try:
            self.collection.remove_item('collection', 'item')
        except KeyError:
            err = True
        self.assertTrue(err)

    def test_remove_item_removes_item(self):
        colid = 'col'
        itemid = 'item'
        self.collection.create_collection(colid)
        self.collection.store_item(colid, 'foo', itemid)
        self.collection.remove_item(colid, itemid)
        self.assertFalse(itemid in self.collection.read_collection(colid))


    def test_remove_collection_expects_collection_to_exist(self):
        err = False
        try:
            self.collection.remove_collection('collection')
        except KeyError:
            err = True
        self.assertTrue(err)

    def test_remove_collection_removes_all_items(self):
        colid = 'col'
        itemid = 'item'
        self.collection.create_collection(colid)
        self.collection.store_item(colid, 'foo', itemid)
        self.collection.remove_collection(colid)
        err = False
        try:
            self.collection.read_collection(colid)
        except KeyError:
            err = True
        self.assertTrue(err)


if "__main__" == __name__:
    unittest.main()
