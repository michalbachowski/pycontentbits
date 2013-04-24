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
from contentbits.storage.abstract import Abstract


class AbstractTestCase(unittest.TestCase):

    def test_read_collection_requires_1_argument(self):
        err = False
        try:
            Abstract().read_collection()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_read_collection_requires_1_argument_1(self):
        err = False
        try:
            Abstract().read_collection(None)
        except NotImplementedError:
            err = True
        self.assertTrue(err)

    def test_store_item_requires_2_arguments(self):
        err = False
        try:
            Abstract().store_item()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_store_item_requires_2_arguments_1(self):
        err = False
        try:
            Abstract().store_item(None)
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_store_item_requires_2_arguments_2(self):
        err = False
        try:
            Abstract().store_item(None, None)
        except NotImplementedError:
            err = True
        self.assertTrue(err)

    def test_store_item_allows_to_pass_3_arguments(self):
        err = False
        err2 = False
        try:
            Abstract().store_item(None, None, item_id=None)
        except TypeError:
            err = True
        except NotImplementedError:
            err2 = True
        self.assertFalse(err)
        self.assertTrue(err2)

    def test_remove_item_requires_2_arguments(self):
        err = False
        try:
            Abstract().remove_item()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_remove_item_requires_2_arguments_1(self):
        err = False
        try:
            Abstract().remove_item(None)
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_remove_item_requires_2_arguments_2(self):
        err = False
        try:
            Abstract().remove_item(None, None)
        except NotImplementedError:
            err = True
        self.assertTrue(err)

    def test_create_collection_requires_no_arguments(self):
        err = False
        try:
            Abstract().create_collection()
        except NotImplementedError:
            err = True
        self.assertTrue(err)

    def test_create_collection_allows_to_pass_one_argument(self):
        err = False
        try:
            Abstract().create_collection(collection_id='abs')
        except NotImplementedError:
            err = True
        self.assertTrue(err)

    def test_remove_collection_requires_1_argument(self):
        err = False
        try:
            Abstract().remove_collection()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_remove_collection_requires_1_argument_1(self):
        err = False
        try:
            Abstract().remove_collection(None)
        except NotImplementedError:
            err = True
        self.assertTrue(err)


if "__main__" == __name__:
    unittest.main()
