#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# python standard library
#
import unittest
import sys

# hack for loading modules
import _path
_path.fix()


##
# content bits modules
#
from contentbits.types import Collection, Item


class CollectionTestCase(unittest.TestCase):

    def test_init_requires_no_arguments(self):
        err = False
        try:
            Collection()
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_init_allows_to_pass_1_argument(self):
        err = False
        try:
            Collection('asd')
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_append_requires_1_argument(self):
        err = False
        try:
            Collection().append()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_append_requires_1_argument_1(self):
        err = False
        try:
            Collection().append('foo')
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_append_returns_instance_of_Collection(self):
        c = Collection()
        self.assertEqual(c.append(None), c)

    def test_append_adds_new_item_to_collection(self):
        c = Collection()
        i = 'foo'
        self.assertEqual(len(list(iter(c))), 0)
        c.append(i)
        self.assertEqual(next(iter(c)), i)

    def test_id_property_returns_given_id_casted_to_string(self):
        self.assertEqual(Collection('asd').id, 'asd')
        self.assertEqual(Collection(1).id, '1')
        self.assertEqual(Collection(1.2).id, '1.2')
        self.assertEqual(Collection(None).id, 'None')

    def test_id_property_is_casted_to_string(self):
        c = Collection()
        c.id = 'asd'
        self.assertEqual(c.id, 'asd')
        c.id = 1
        self.assertEqual(c.id, '1')
        c.id = 1.2
        self.assertEqual(c.id, '1.2')
        c.id = None
        self.assertEqual(c.id, 'None')

    def test_contains_checkt_whether_collection_contains_given_item(self):
        c = Collection()
        i = Item(None, 1)
        self.assertFalse(i in c)
        c.append(i)
        self.assertTrue(i in c)

    def test_iter_returns_iterator_that_goes_througth_items(self):
        c = Collection()
        i1 = 1
        i2 = '2'
        c.append(i1).append(i2)
        iterator = iter(c)
        self.assertEqual(next(iterator), i1)
        self.assertEqual(next(iterator), i2)

    def test_collections_are_compared_using_only_id(self):
        c1 = Collection(1)
        c2 = Collection(2)
        i = 1
        self.assertNotEqual(c1, c2)
        c2.id = 1
        self.assertEqual(c1, c2)
        c1.append(i)
        self.assertEqual(c1, c2)

    def test_collection_can_be_compared_to_string(self):
        c = Collection(1)
        self.assertEqual(c, 1)
        self.assertEqual(c, '1')
        if sys.version_info[0] == 3:
            self.assertEqual('1', c)
        else:
            self.assertNotEqual('1', c)

    def test_str_returns_collection_id(self):
        c = Collection(1)
        self.assertEqual(str(c), '1')

    def test_del_allows_to_delete_item_class_instance(self):
        i = Item(None, 1)
        c = Collection()
        c.append(i)
        self.assertTrue(i in c)
        del c[i]
        self.assertFalse(i in c)

    def test_del_can_remove_item_by_id(self):
        i = Item(None, 1)
        c = Collection()
        c.append(i)
        self.assertTrue(i in c)
        del c[i.id]
        self.assertFalse(i in c)

    def test_del_raises_ValueError_when_item_was_not_found_in_list(self):
        c = Collection()
        i = Item(None, 1)
        err = False
        try:
            del c[i]
        except ValueError:
            err = True
        self.assertTrue(err)


class ItemTestCase(unittest.TestCase):

    def test_init_requires_1_argument(self):
        err = False
        try:
            Item()
        except TypeError:
            err = True
        self.assertTrue(err)

    def test_init_requires_1_argument_1(self):
        err = False
        try:
            Item('asd')
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_init_allows_to_pass_2_arguments(self):
        err = False
        try:
            Item('asd', 'foo')
        except TypeError:
            err = True
        self.assertFalse(err)

    def test_id_property_returns_given_id_casted_to_string(self):
        self.assertEqual(Item(None, 'asd').id, 'asd')
        self.assertEqual(Item(None, 1).id, '1')
        self.assertEqual(Item(None, 1.2).id, '1.2')
        self.assertEqual(Item(None, None).id, 'None')

    def test_id_property_is_casted_to_string(self):
        c = Item(None)
        c.id = 'asd'
        self.assertEqual(c.id, 'asd')
        c.id = 1
        self.assertEqual(c.id, '1')
        c.id = 1.2
        self.assertEqual(c.id, '1.2')
        c.id = None
        self.assertEqual(c.id, 'None')

    def test_data_property_returns_given_data(self):
        self.assertEqual(Item(None).data, None)
        self.assertEqual(Item(2).data, 2)
        self.assertEqual(Item([2,3]).data, [2,3])

    def test_data_property_allows_to_set_data(self):
        i = Item(None)
        self.assertEqual(i.data, None)
        i.data = 2
        self.assertEqual(i.data, 2)
        i.data = [2,3]
        self.assertEqual(i.data, [2,3])

    def test_items_are_compared_using_only_id(self):
        i1 = Item(None, 1)
        i2 = Item(None, 2)
        data = 1
        self.assertNotEqual(i1, i2)
        i2.id = 1
        self.assertEqual(i1, i2)
        i1.data = data
        self.assertEqual(i1, i2)

    def test_item_can_be_compared_to_string(self):
        i = Item(None, 1)
        self.assertEqual(i, 1)
        self.assertEqual(i, '1')
        if sys.version_info[0] == 3:
            self.assertEqual('1', i)
        else:
            self.assertNotEqual('1', i)


if "__main__" == __name__:
    unittest.main()
