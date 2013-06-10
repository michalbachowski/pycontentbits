#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
from functools import partial


##
# content bits modules
#
from contentbits.storage.abstract import Abstract


class AbstractTestCase(unittest.TestCase):

    def setUp(self):
        self.a = Abstract()

    def test_read_collection_requires_1_argument(self):
        self.assertRaises(TypeError, self.a.read_collection)

    def test_read_collection_requires_1_argument_1(self):
        self.assertRaises(NotImplementedError,
                partial(self.a.read_collection, None))

    def test_store_item_requires_2_arguments(self):
        self.assertRaises(TypeError, self.a.store_item)

    def test_store_item_requires_2_arguments_1(self):
        self.assertRaises(TypeError, partial(self.a.store_item, None))

    def test_store_item_requires_2_arguments_2(self):
        self.assertRaises(NotImplementedError,
                partial(self.a.store_item, None, None))

    def test_store_item_allows_to_pass_3_arguments(self):
        self.assertRaises(NotImplementedError, partial(Abstract().store_item,
                None, None, item_id=None))

    def test_remove_item_requires_2_arguments(self):
        self.assertRaises(TypeError, Abstract().remove_item)

    def test_remove_item_requires_2_arguments_1(self):
        self.assertRaises(TypeError, partial(Abstract().remove_item, None))

    def test_remove_item_requires_2_arguments_2(self):
        self.assertRaises(NotImplementedError, partial(Abstract().remove_item,
                None, None))

    def test_create_collection_requires_no_arguments(self):
        self.assertRaises(NotImplementedError, Abstract().create_collection)


    def test_create_collection_allows_to_pass_one_argument(self):
        self.assertRaises(NotImplementedError,
                partial(Abstract().create_collection, 'abs'))

    def test_remove_collection_requires_1_argument(self):
        self.assertRaises(TypeError, Abstract().remove_collection)

    def test_remove_collection_requires_1_argument_1(self):
        self.assertRaises(NotImplementedError,
                partial(Abstract().remove_collection, None))


if "__main__" == __name__:
    unittest.main()
