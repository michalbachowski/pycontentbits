#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest

##
# test utilities
#
from testutils import mock, IsA

##
# PyPromise modules
#
from promise import Promise

##
# content bits modules
#
from contentbits.storage.memory import Memory


class MemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.storage = Memory()
        self.c = mock.MagicMock()

    def _idx(self, deferred, callback=None):
        if callback is None:
            callback = mock.MagicMock()
        deferred.done(callback)
        return callback.call_args[0][0]

    def test_create_collection_returns_instance_of_promise(self):
        self.assertIsInstance(self.storage.create_collection(), Promise)

    def test_create_collection_returns_collection_id(self):
        self.storage.create_collection().done(self.c)
        self.c.assert_called_once_with(mock.ANY)

    def test_create_collection_does_nothing_when_collection_exists(self):
        idx = self._idx(self.storage.create_collection())
        idxb = self._idx(self.storage.store_item(idx, 'b'))[1]
        idx2 = self._idx(self.storage.create_collection(idx))
        self.assertEqual(idx, idx2)
        self.storage.read_collection(idx).done(self.c)
        self.c.assert_called_once_with({idxb: 'b'})

    def test_create_collection_generates_unique_id_for_item(self):
        idx1 = self._idx(self.storage.create_collection(0).done(self.c))
        idx2 = self._idx(self.storage.create_collection().done(self.c))
        self.assertNotEqual(idx1, idx2)

    def test_read_collection_returns_instance_of_promise(self):
        self.assertIsInstance(self.storage.read_collection(1), Promise)

    def test_read_collection_raises_key_error_for_non_existing_collection(self):
        self.storage.read_collection('foo').fail(self.c).done(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))


    def test_read_collection_returns_dict_for_existing_collection(self):
        idx = self._idx(self.storage.create_collection())
        self.storage.read_collection(idx).done(self.c)
        self.c.assert_called_once_with({})

    def test_read_collection_returns_item_added_to_collection(self):
        idx = self._idx(self.storage.create_collection())
        idxa = self._idx(self.storage.store_item(idx, 'a'))[1]
        idxb = self._idx(self.storage.store_item(idx, 'b'))[1]
        self.storage.read_collection(idx).done(self.c)
        self.c.assert_called_once_with({idxa: 'a', idxb: 'b'})

    def test_store_item_expects_collection_to_exist(self):
        self.storage.store_item('foo', None).fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_store_item_returns_item_id(self):
        idx = self._idx(self.storage.create_collection())
        idxc = self.storage.store_item(idx, None)
        self.assertIsNotNone(idxc)

    def test_remove_item_expects_collection_to_exist(self):
        self.storage.remove_item('collection', 'item').fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_remove_item_returns_id_of_removed_collection_and_item(self):
        idx = self._idx(self.storage.create_collection())
        idxi = self._idx(self.storage.store_item(idx, None))[1]
        self.storage.remove_item(idx, idxi).done(self.c)
        self.c.assert_called_once_with((idx, idxi))

    def test_remove_item_removes_item(self):
        colid = 'col'
        itemid = 'item'
        self.storage.create_collection(colid)
        self.storage.store_item(colid, 'foo', itemid)
        self.storage.remove_item(colid, itemid)
        self.storage.read_collection(colid).done(self.c)
        self.c.assert_called_once_with({})

    def test_remove_collection_expects_collection_to_exist(self):
        self.storage.remove_collection('collection').fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_remove_collection_returns_id_of_removed_collection(self):
        idx = self._idx(self.storage.create_collection())
        self.storage.remove_collection(idx).done(self.c)
        self.c.assert_called_once_with(idx)

    def test_remove_collection_removes_all_items(self):
        colid = 'col'
        itemid = 'item'
        self.storage.create_collection(colid)
        self.storage.store_item(colid, 'foo', itemid)
        self.storage.remove_collection(colid)
        self.storage.read_collection(colid).fail(self.c)
        self.c.assert_called_once_with(exception=IsA(KeyError))

    def test_store_item_generates_unique_item_id(self):
        self.storage.create_collection('a')
        idx1 = self._idx(self.storage.store_item('a', None, 0))[1]
        idx2 = self._idx(self.storage.store_item('a', None))[1]
        self.assertNotEqual(idx1, idx2)

    def test_store_item_generates_item_id_unique_to_given_collection(self):
        self.storage.create_collection('a')
        self.storage.create_collection('b')
        idx1 = self._idx(self.storage.store_item('a', None, 0))
        idx2 = self._idx(self.storage.store_item('b', None))
        self.assertEqual(idx1[1], idx2[1])


if "__main__" == __name__:
    unittest.main()
