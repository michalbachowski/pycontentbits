#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial

# hack for loading modules
from _path import fix, mock
fix()

##
# test helper
#
from mock_helper import IsA

##
# content bits modules
#
from contentbits.manager import Manager


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.storage = mock.MagicMock()
        self.factory = mock.MagicMock()
        self.collection = mock.MagicMock()
        self.collection.id = 1
        self.manager = Manager(self.storage, self.factory)

    def test_init_allows_to_pass_2_arguments(self):
        err = False
        try:
            Manager(None)
            Manager(None, None)
            Manager(storage=None, collection_factory=None)
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_set_storage_sets_storage_to_be_used(self):
        storage = mock.MagicMock()
        storage.store_item = mock.MagicMock()
        item = mock.MagicMock()
        item.id = None
        item.data = None
        Manager().set_storage(storage).add_item_to_collection(None, item)
        storage.store_item.assert_called_once_with(None, None, None)

    def test_set_collection_factory_sets_collection_factory_to_be_used(self):
        collection = mock.MagicMock()
        cf = mock.MagicMock()
        cf.discover = mock.MagicMock(return_value=collection)
        self.storage.read_collection = mock.MagicMock(return_value={'a': 1})
        c = Manager(self.storage).set_collection_factory(cf).read_collection(
                None)
        self.assertIsNone(c.id)
        cf.discover.assert_called_once_with({'a': 1})

    def test_read_collection_uses_factory_and_storage(self):
        self.storage.read_collection = mock.MagicMock(return_value={'a': 1})
        self.factory.discover = mock.MagicMock(return_value=self.collection)
        c = self.manager.read_collection(1)
        self.storage.read_collection.assert_called_once_with(1)
        self.factory.discover.assert_called_once_with({'a': 1})
        self.assertEqual(c, self.collection)

    def test_read_collection_appends_id(self):
        self.storage.read_collection = mock.MagicMock(return_value={'a': 1})
        self.factory.discover = mock.MagicMock(return_value=self.collection)
        c = self.manager.read_collection(1)
        self.assertEqual(c.id, 1)

    def test_read_collection_returns_collection_when_no_collection_found(self):

        self.storage.read_collection = mock.MagicMock(side_effect=KeyError())
        self.factory.discover = mock.MagicMock(return_value=self.collection)
        c = self.manager.read_collection(1)
        self.assertEqual(c.id, 1)

    def test_remove_collection_uses_storage(self):
        self.storage.remove_collection = mock.MagicMock()
        self.manager.remove_collection(1)
        self.storage.remove_collection.assert_called_once_with(1)

    def test_remove_item_from_collection_uses_storage(self):
        self.storage.remove_item = mock.MagicMock()
        self.manager.remove_item_from_collection(1, 2)
        self.storage.remove_item.assert_called_once_with(1, 2)

    def test_add_item_to_collection_uses_storage(self):
        self.storage.store_item = mock.MagicMock()
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        self.manager.add_item_to_collection(1, item)
        self.storage.store_item.assert_called_once_with(1, 'foo', 2)

    def test_add_item_to_collection_returns_what_storage_returned(self):
        self.storage.store_item = mock.MagicMock(return_value=3)
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        self.assertEqual(self.manager.add_item_to_collection(1, item), 3)

    def test_save_collection_requires_1_argument(self):
        self.assertRaises(TypeError, self.manager.save_collection)

    def test_save_collection_requires_1_argument_1(self):
        self.assertRaises(AttributeError,
                partial(self.manager.save_collection, None))

    def test_save_collection_expects_object_with_id_attribute(self):
        self.assertRaises(AttributeError,
                partial(self.manager.save_collection, None))
        err = False
        try:
            self.manager.save_collection(self.collection)
        except:
            err = True
        self.assertFalse(err)

    def test_save_collection_expects_iterable_object(self):
        self.collection.__iter__ = mock.MagicMock(return_value=iter([]))
        self.manager.save_collection(self.collection)
        self.collection.__iter__.assert_called_once_with()

    def test_save_collection_reads_collection_from_storage(self):
        self.storage.read_collection = mock.MagicMock(return_value=iter([]))
        self.manager.save_collection(self.collection)
        self.storage.read_collection.assert_called_once_with(self.collection.id)

    def test_save_collection_creates_collection_when_not_found(self):
        self.storage.read_collection = mock.MagicMock(side_effect=KeyError())
        self.storage.create_collection = mock.MagicMock(
                return_value=self.collection.id)
        self.manager.save_collection(self.collection)
        self.storage.read_collection.assert_called_once_with(self.collection.id)
        self.storage.create_collection.assert_called_once_with(
                self.collection.id)

    def test_save_collection_stores_new_items(self):
        # prepare
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        self.collection.__iter__ = mock.MagicMock(return_value=iter([item]))
        self.storage.read_collection = mock.MagicMock(return_value={})
        self.storage.store_item = mock.MagicMock()
        # test
        self.manager.save_collection(self.collection)
        # verify
        self.storage.store_item.assert_called_once_with(1, 'foo', 2)

    def test_save_collection_removes_old_items_from_collection(self):
        # prepare
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        c = mock.MagicMock()
        c.__iter__ = mock.MagicMock(return_value=iter([item]))
        self.factory.discover = mock.MagicMock(return_value=c)
        self.storage.remove_item = mock.MagicMock()
        # test
        self.manager.save_collection(self.collection)
        # verify
        self.storage.remove_item.assert_called_once_with(1, 2)

    def test_save_collection_removes_only_old_items_from_collection(self):
        # prepare
        item = mock.MagicMock()
        item.id = 2
        c = mock.MagicMock()
        c.__delitem__ = mock.MagicMock(side_effect=ValueError())
        self.collection.__iter__ = mock.MagicMock(return_value=iter([item]))
        self.factory.discover = mock.MagicMock(return_value=c)
        # test
        self.manager.save_collection(self.collection)
        # verify
        c.__delitem__.assert_called_once_with(item)


if "__main__" == __name__:
    unittest.main()
