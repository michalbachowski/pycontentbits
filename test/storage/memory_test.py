#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial

##
# test utilities
#
from testutils import mock, IsA


##
# content bits modules
#
from promise import Promise
from contentbits.storage.memory import Memory


class MemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.collection = Memory()
        self.c = mock.MagicMock()

    def _idx(self, deferred, callback=None):
        if callback is None:
            callback = mock.MagicMock()
        deferred.done(callback)
        idx = callback.call_args[0][0]
        return idx

    def test_create_collection_returns_instance_of_promise(self):
        self.assertIsInstance(self.collection.create_collection(), Promise)

    def test_create_collection_returns_collection_id(self):
        self.collection.create_collection().done(self.c)
        self.c.assert_called_once_with(mock.ANY)

    def test_create_collection_does_nothing_when_collection_Exists(self):
        idx = self._idx(self.collection.create_collection())
        idxb = self._idx(self.collection.store_item(idx, 'b'))
        idx2 = self._idx(self.collection.create_collection(idx))
        self.assertEqual(idx, idx2)
        self.collection.read_collection(idx).done(self.c)
        self.c.assert_called_once_with({idxb: 'b'})

    def test_create_collection_generates_unique_id_for_item(self):
        idx1 = self._idx(self.collection.create_collection(0).done(self.c))
        idx2 = self._idx(self.collection.create_collection().done(self.c))
        self.assertNotEqual(idx1, idx2)

    def test_read_collection_returns_instance_of_promise(self):
        self.assertIsInstance(self.collection.read_collection(1), Promise)

    def test_read_collection_raises_key_error_for_non_existing_collection(self):
        self.collection.read_collection('foo').fail(self.c).done(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))


    def test_read_collection_returns_dict_for_existing_collection(self):
        idx = self._idx(self.collection.create_collection())
        self.collection.read_collection(idx).done(self.c)
        self.c.assert_called_once_with({})

    def test_read_collection_returns_item_added_to_collection(self):
        idx = self._idx(self.collection.create_collection())
        idxa = self._idx(self.collection.store_item(idx, 'a'))
        idxb = self._idx(self.collection.store_item(idx, 'b'))
        self.collection.read_collection(idx).done(self.c)
        self.c.assert_called_once_with({idxa: 'a', idxb: 'b'})

    def test_store_item_expects_collection_to_exist(self):
        self.collection.store_item('foo', None).fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_store_item_returns_item_id(self):
        idx = self._idx(self.collection.create_collection())
        idxc = self.collection.store_item(idx, None)
        self.assertIsNotNone(idxc)

    def test_remove_item_expects_collection_to_exist(self):
        self.collection.remove_item('collection', 'item').fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_remove_item_returns_id_of_removed_collection_and_item(self):
        idx = self._idx(self.collection.create_collection())
        idxi = self._idx(self.collection.store_item(idx, None))
        self.collection.remove_item(idx, idxi).done(self.c)
        self.c.assert_called_once_with((idx, idxi))

    def test_remove_item_removes_item(self):
        colid = 'col'
        itemid = 'item'
        self.collection.create_collection(colid)
        self.collection.store_item(colid, 'foo', itemid)
        self.collection.remove_item(colid, itemid)
        self.collection.read_collection(colid).done(self.c)
        self.c.assert_called_once_with({})

    def test_remove_collection_expects_collection_to_exist(self):
        self.collection.remove_collection('collection').fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_remove_collection_returns_id_of_removed_collection(self):
        idx = self._idx(self.collection.create_collection())
        self.collection.remove_collection(idx).done(self.c)
        self.c.assert_called_once_with(idx)

    def test_remove_collection_removes_all_items(self):
        colid = 'col'
        itemid = 'item'
        self.collection.create_collection(colid)
        self.collection.store_item(colid, 'foo', itemid)
        self.collection.remove_collection(colid)
        self.collection.read_collection(colid).fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_store_item_generates_unique_item_id(self):
        self.collection.create_collection('a')
        idx1 = self.collection.store_item('a', None, 0)
        idx2 = self.collection.store_item('a', None)
        self.assertNotEqual(idx1, idx2)

    def test_store_item_generates_item_id_unique_to_given_collection(self):
        self.collection.create_collection('a')
        self.collection.create_collection('b')
        idx1 = self._idx(self.collection.store_item('a', None, 0))
        idx2 = self._idx(self.collection.store_item('b', None))
        self.assertEqual(idx1, idx2)


if "__main__" == __name__:
    unittest.main()
