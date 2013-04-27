#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial

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
        self.assertRaises(KeyError, partial(self.collection.read_collection,
                'foo'))

    def test_create_collection_returns_collection_id(self):
        self.assertIsNotNone(self.collection.create_collection())

    def test_create_collection_does_nothing_when_collection_Exists(self):
        idx = self.collection.create_collection()
        idxb = self.collection.store_item(idx, 'b')
        self.assertEqual(self.collection.create_collection(idx), idx)
        c = self.collection.read_collection(idx)
        self.assertTrue(idxb in c)
        self.assertEqual(c[idxb], 'b')

    def test_create_collection_generates_unique_id_for_item(self):
        idx1 = self.collection.create_collection(0)
        idx2 = self.collection.create_collection()
        self.assertNotEqual(idx1, idx2)

    def test_read_collection_returns_dict_for_existing_collection(self):
        idx = self.collection.create_collection()
        self.assertEqual(self.collection.read_collection(idx), {})

    def test_read_collection_returns_item_added_to_collection(self):
        idx = self.collection.create_collection()
        idxa = self.collection.store_item(idx, 'a')
        idxb = self.collection.store_item(idx, 'b')
        c = self.collection.read_collection(idx)
        self.assertTrue(idxa in c)
        self.assertTrue(idxb in c)
        self.assertEqual(c[idxa], 'a')
        self.assertEqual(c[idxb], 'b')

    def test_store_item_expects_collection_to_exist(self):
        self.assertRaises(KeyError, partial(self.collection.store_item, 'foo',
                None))

    def test_store_item_returns_item_id(self):
        idx = self.collection.create_collection()
        self.assertIsNotNone(self.collection.store_item(idx, None))

    def test_remove_item_expects_collection_to_exist(self):
        self.assertRaises(KeyError, partial(self.collection.remove_item,
                'collection', 'item'))

    def test_remove_item_removes_item(self):
        colid = 'col'
        itemid = 'item'
        self.collection.create_collection(colid)
        self.collection.store_item(colid, 'foo', itemid)
        self.collection.remove_item(colid, itemid)
        self.assertFalse(itemid in self.collection.read_collection(colid))


    def test_remove_collection_expects_collection_to_exist(self):
        self.assertRaises(KeyError, partial(self.collection.remove_collection,
                'collection'))

    def test_remove_collection_removes_all_items(self):
        colid = 'col'
        itemid = 'item'
        self.collection.create_collection(colid)
        self.collection.store_item(colid, 'foo', itemid)
        self.collection.remove_collection(colid)
        self.assertRaises(KeyError, partial(self.collection.read_collection,
                colid))

    def test_store_item_generates_unique_item_id(self):
        self.collection.create_collection('a')
        idx1 = self.collection.store_item('a', None, 0)
        idx2 = self.collection.store_item('a', None)
        self.assertNotEqual(idx1, idx2)

    def test_store_item_generates_item_id_unique_to_given_collection(self):
        self.collection.create_collection('a')
        self.collection.create_collection('b')
        idx1 = self.collection.store_item('a', None, 0)
        idx2 = self.collection.store_item('b', None)
        self.assertEqual(idx1, idx2)


if "__main__" == __name__:
    unittest.main()
