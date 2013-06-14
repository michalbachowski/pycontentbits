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
from testutils import mock, IsCallable

##
# promise
#
from promise import Promise

##
# content bits modules
#
from contentbits.manager import Manager
from contentbits.factory import CollectionFactory


class ManagerTestCase(unittest.TestCase):

    def setUp(self):
        # set defaul exception name for "fail_side_effect"
        self.exception = KeyError()

        # setup promise
        self.promise = mock.MagicMock()
        self.promise.done = mock.MagicMock(side_effect=lambda a:
                [a({'a': 1}), self.promise][1])

        # setup storage
        self.storage = mock.MagicMock()
        self.storage.read_collection = mock.MagicMock(return_value=self.promise)

        promise = mock.MagicMock()
        promise.done = lambda a: [a(self.collection.id), self.promise][1]
        self.storage.create_collection = mock.MagicMock(return_value=promise)

        # setup collection
        self.collection = mock.MagicMock()
        self.collection.id = 1

        # setup factory
        self.factory = mock.MagicMock()
        self.factory.discover = mock.MagicMock(return_value=self.collection)

        # setup manager
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
        self.assertEqual(Manager().set_storage(self.storage).storage, self.storage)

    def test_storage_defaults_to_None(self):
        self.assertIsNone(Manager().storage)

    def test_storage_returns_previously_set_storage(self):
        self.assertEqual(Manager().set_storage('foo').storage, 'foo')

    def test_set_collection_factory_sets_collection_factory_to_be_used(self):
        Manager(self.storage).set_collection_factory(self.factory).read_collection(None)
        self.factory.discover.assert_called_once_with({'a': 1})

    def test_collection_factory_defaults_to_CollectionFactory(self):
        self.assertIsInstance(Manager().collection_factory, CollectionFactory)

    def test_collection_factory_returns_previously_set_collection_factory(self):
        self.assertEqual(Manager().set_collection_factory('foo').collection_factory, 'foo')

    def test_read_collection_uses_factory_and_storage(self):
        self.manager.read_collection(1)
        self.storage.read_collection.assert_called_once_with(1)
        self.factory.discover.assert_called_once_with({'a': 1})

    def test_read_collection_appends_id(self):
        self.manager.read_collection(1)
        self.assertEqual(self.collection.id, 1)

    def test_read_collection_returns_collection_when_no_collection_found(self):
        # turn off default behavious for "done" callback
        self.promise.done = lambda a: self.promise
        self.promise.fail = mock.MagicMock(side_effect=lambda a:
                [a(exception=self.exception), self.promise][1])
        self.manager.read_collection(1)
        self.assertEqual(self.collection.id, 1)

    def test_remove_collection_expects_one_argument(self):
        self.assertRaises(TypeError, self.manager.remove_collection)

    def test_remove_collection_uses_storage(self):
        self.storage.remove_collection = mock.MagicMock()
        self.manager.remove_collection(1)
        self.storage.remove_collection.assert_called_once_with(1)

    def test_remove_item_from_collection_uses_storage(self):
        self.storage.remove_item = mock.MagicMock()
        self.manager.remove_item_from_collection(1, 2)
        self.storage.remove_item.assert_called_once_with(1, 2)

    def test_add_item_to_collection_expects_Collection_and_Item_instance(self):
        self.assertRaises(AttributeError,
                partial(self.manager.add_item_to_collection, None, None))
        self.assertRaises(AttributeError,
                partial(self.manager.add_item_to_collection, self.collection,
                        None))
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        self.assertIsNotNone(partial(self.manager.add_item_to_collection,
                self.collection, item))

    def test_add_item_to_collection_uses_storage(self):
        self.storage.store_item = mock.MagicMock()
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        self.manager.add_item_to_collection(self.collection, item)
        self.storage.store_item.assert_called_once_with(1, 'foo', 2)

    def test_add_item_to_collection_returns_promise(self):
        self.storage.store_item = mock.MagicMock(return_value=self.promise)
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        self.assertIsInstance(self.manager.add_item_to_collection(
                self.collection, item), Promise)

    def test_save_collection_requires_1_argument(self):
        self.assertRaises(TypeError, self.manager.save_collection)

    def test_save_collection_requires_1_argument_1(self):
        self.assertRaises(TypeError,
                partial(self.manager.save_collection, None))

    def test_save_collection_expects_iterable_object(self):
        self.assertRaises(TypeError,
                partial(self.manager.save_collection, None))

    def test_save_collection_expects_object_with_id_attribute(self):
        del self.collection.id
        self.assertRaises(AttributeError,partial(self.manager.save_collection,
                self.collection))

    def test_save_collection_reads_collection_from_storage(self):
        self.factory.discover.return_value = iter([])
        self.manager.save_collection(self.collection)
        self.storage.read_collection.assert_called_once_with(self.collection.id)

    def test_save_collection_creates_collection_when_not_found(self):
        self.factory.discover.return_value = iter([])
        self.promise.done = lambda a: self.promise
        self.promise.fail = mock.MagicMock(side_effect=lambda a:
                [a(exception=self.exception), self.promise][1])
        self.manager.save_collection(self.collection)
        self.storage.read_collection.assert_called_once_with(self.collection.id)
        self.storage.create_collection.assert_called_once_with(self.collection.id)

    def test_save_collection_stores_new_items(self):
        # prepare
        item = mock.MagicMock()
        item.id = 2
        item.data = 'foo'
        self.collection.__iter__ = lambda a: iter([item])
        self.promise.done = lambda a: [a({}), self.promise][1]
        self.storage.read_collection = lambda a: self.promise
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
        items = iter([item])

        self.storage.read_collection = mock.MagicMock(return_value=self.promise)
        self.factory.discover.return_value = items

        # test
        self.manager.save_collection(self.collection)

        # verify
        self.storage.read_collection.assert_called_once_with(1)
        self.promise.done.assert_called_once_with(IsCallable())
        self.factory.discover.assert_called_once_with({'a': 1})
        self.storage.store_item.assert_not_called()
        self.storage.remove_item.assert_called_once_with(self.collection.id, item.id)


if "__main__" == __name__:
    unittest.main()
