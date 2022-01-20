#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import channel
from channel import Channel
import unittest
import uuid


class Test(unittest.TestCase):
    def test_init(self):
        # test the init constructor
        self.assertNotEqual(Channel("id2", "channel_test_init", "channel_admin", channel.Group("group1"), ["moi", "toi"]),
                            Channel("id2", "channel_test_init", "channel_admin", channel.Group("group1"), ["toi", "moi"]))
        self.assertIsInstance(Channel(str(uuid.uuid4()), "channel_test_init", "channel_admin", channel.Group("group1"),
                                      ["moi", "toi"]), Channel)
        self.assertNotEqual(Channel(str(uuid.uuid4()), "channel_test_init", "channel_admin", channel.Group("group1"),
                                    ["moi", "toi"]),
                            Channel(str(uuid.uuid4()), "channel_test_init", "channel_admin", channel.Group("group1"),
                                    ["moi", "toi"]))
        with self.assertRaises(AssertionError):
            Channel(10, "channel_test_init", "channel_admin", channel.Group("group1"), ["moi", "toi"])
        with self.assertRaises(AssertionError):
            Channel("id4", "channel_test_init", "channel_admin", "goup2", ["moi", "toi"])
        with self.assertRaises(AssertionError):
            Channel("id5", "channel_test_init", "channel_admin", channel.Group("group1"), 24)
        with self.assertRaises(AssertionError):
            Channel("id6", "channel_test_init", "channel_admin", channel.Group("group1"), ["moi", 23])

    """def test_add_member(self):
        #test the add_member method
        self.assertEqual(Channel("id3", "channel_test_init", "channel_admin", channel.Group("group1"),
                                 ["moi"]).add_member("toi"),
                         Channel("id3", "channel_test_init", "channel_admin", channel.Group("group1"), ["moi", "toi"]))

    def test_remove_member(self):
        #test the remove_member method
        pass

    def test_errors(self):
        # test the errors cases"""

if __name__ == '__main__':
    unittest.main()