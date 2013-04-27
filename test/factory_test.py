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
from contentbits.factory import CollectionFactory


class CollectionFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.collection = mock.MagicMock()
        self.collection.return_value=self.collection
        self.collection.append = mock.MagicMock()
        self.item = mock.MagicMock()
        self.cf = CollectionFactory(self.collection, self.item)

    def test_init_requires_no_arguments(self):
        err = False
        try:
            CollectionFactory()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_init_allows_2_arguments(self):
        err = False
        try:
            CollectionFactory(None)
            CollectionFactory(None, None)
        except TypeError:
            err = True
        self.assertFalse(err)

# from dict
    def test_from_dict_expects_dict(self):
        d = mock.MagicMock()
        d.items = mock.MagicMock(return_value=[(0,1)])
        CollectionFactory().from_dict(d)
        d.items.assert_called_once_with()

    def test_from_dict_uses_given_collection_class(self):
        self.cf.from_dict({'a': 1})
        self.collection.assert_called_once_with()
        self.collection.append.assert_called_once_with(IsA(mock.MagicMock))

    def test_from_dict_uses_given_item_class(self):
        self.cf.from_dict({'a': 1})
        self.item.assert_called_once_with(1, 'a')

    def test_from_dict_returns_collection(self):
        self.assertEqual(self.cf.from_dict({'a': 1}), self.collection)

# from_list
    def test_from_list_expects_list(self):
        CollectionFactory().from_list([1])

    def test_from_list_uses_given_collection_class(self):
        self.cf.from_list([1])
        self.collection.assert_called_once_with()
        self.collection.append.assert_called_once_with(IsA(mock.MagicMock))

    def test_from_list_uses_given_item_class(self):
        self.cf.from_list([1])
        self.item.assert_called_once_with(1, None)

    def test_from_list_returns_collection(self):
        self.assertEqual(self.cf.from_list([1]), self.collection)

# from_iterator
    def test_from_iterator_expects_iterator(self):
        CollectionFactory().from_iterator((i for i in [1]))

    def test_from_iterator_uses_given_collection_class(self):
        self.cf.from_iterator((i for i in [1]))
        self.collection.assert_called_once_with()
        self.collection.append.assert_called_once_with(IsA(mock.MagicMock))

    def test_from_iterator_uses_given_item_class(self):
        self.cf.from_iterator((i for i in [1]))
        self.item.assert_called_once_with(1, None)

    def test_from_iterator_returns_collection(self):
        self.assertEqual(self.cf.from_iterator([1]), self.collection)

# from_iterator_with_tuples
    def test_from_iterator_with_tuples_expects_iterator_with_tuples(self):
        self.assertRaises(TypeError, partial(
                CollectionFactory().from_iterator_with_tuples,
                (i for i in [1])))

    def test_from_iterator_with_tuples_expects_iterator_with_tuples_1(self):
        CollectionFactory().from_iterator_with_tuples((i for i in [('a', 1)]))

    def test_from_iterator_with_tuples_uses_given_collection_class(self):
        self.cf.from_iterator_with_tuples((i for i in [('a', 1)]))
        self.collection.assert_called_once_with()
        self.collection.append.assert_called_once_with(IsA(mock.MagicMock))

    def test_from_iterator_with_tuples_uses_given_item_class(self):
        self.cf.from_iterator_with_tuples((i for i in [('a', 1)]))
        self.item.assert_called_once_with(1, 'a')

    def test_from_iterator_with_tuples_returns_collection(self):
        self.assertEqual(self.cf.from_iterator_with_tuples(
                (i for i in [('a', 1)])), self.collection)

# discover
    def test_discover_requires_1_argument(self):
        self.assertRaises(TypeError, CollectionFactory().discover)

    def test_discover_uses_given_collection_class(self):
        self.cf.discover({'a:': 1})
        self.collection.assert_called_once_with()
        self.collection.append.assert_called_once_with(IsA(mock.MagicMock))

    def test_discover_uses_given_item_class(self):
        self.cf.discover([1])
        self.item.assert_called_once_with(1, None)

    def test_discover_returns_collection(self):
        self.assertEqual(self.cf.discover([1]), self.collection)

    def test_discover_accepts_dict(self):
        self.cf.discover({'b': 2})
        self.collection.assert_called_once()
        self.item.assert_called_once_with(2, 'b')

    def test_discover_accepts_list(self):
        self.cf.discover([1])
        self.collection.assert_called_once()
        self.item.assert_called_once_with(1, None)

    def test_discover_accepts_iterator(self):
        self.cf.foo = 1
        self.cf.discover((i for i in [1]))
        self.collection.assert_called_trice()
        self.item.assert_called_once_with(1, None)

    def test_discover_accepts_iterator_with_touple(self):
        self.cf.discover((i for i in [('a', 1)]))
        self.collection.assert_called_trice()
        self.item.assert_called_once_with(1, 'a')


if "__main__" == __name__:
    unittest.main()
