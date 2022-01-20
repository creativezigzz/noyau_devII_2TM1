#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import src.models.channel
from src.models.channel import Channel
import unittest
import uuid


class Test(unittest.TestCase):
    def test_init(self):
        # test the init constructor
        self.assertNotEqual(
            Channel("id2", "channel_test_init", "channel_admin", channel.Group("group1"), ["moi", "toi"]),
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
            Channel("id3", "channel_test_init", "channel_admin", "goup2", ["moi", "toi"])
        with self.assertRaises(AssertionError):
            Channel("id4", "channel_test_init", "channel_admin", channel.Group("group1"), 24)
        with self.assertRaises(AssertionError):
            Channel("id5", "channel_test_init", "channel_admin", channel.Group("group1"), ["moi", 23])

    def test_add_member(self):
        """test the add_member method"""
        with self.assertRaises(TypeError):
            Channel("id6", "channel_test_add", "channel_admin", channel.Group("group1"), ["moi", "toi"]).add_member()
        with self.assertRaises(TypeError):
            Channel("id7", "channel_test_add", "channel_admin",
                    channel.Group("group1"), ["moi", "toi"]).add_member("toto", "tutu")
        with self.assertRaises(channel.WrongTypeException):
            Channel("id6", "channel_test_add", "channel_admin", channel.Group("group1"), ["moi", "toi"]).add_member(24)
        channel_a = Channel("id7", "channel_test_add", "channel_admin", channel.Group("group1"), ["moi", "toi"])
        channel_a.add_member("toto")
        self.assertEqual(channel_a.channel_members, ["moi", "toi", "channel_admin", "toto"])

    def test_remove_member(self):
        """test the remove_member method"""
        with self.assertRaises(TypeError):
            Channel("id8", "channel_test_remove", "channel_admin", channel.Group("group1"), ["moi", "toi"]).remove_member()
        with self.assertRaises(channel.WrongTypeException):
            Channel("id9", "channel_test_remove", "channel_admin", channel.Group("group1"), ["moi", "toi"]).remove_member(
                18)
        with self.assertRaises(TypeError):
            Channel("id10", "channel_test_remove", "channel_admin", channel.Group("group1"), ["moi", "toi"]).remove_member(
                "toi", "moi")
        with self.assertRaises(channel.ParamNotFoundException):
            Channel("id11", "channel_test_remove", "channel_admin", channel.Group("group1"), ["moi", "toi"]).remove_member(
                "toto")
        with self.assertRaises(channel.WrongTypeException):
            Channel("id12", "channel_test_remove", "channel_admin", channel.Group("group1"), []).remove_member(
                ["channel_admin"])
        channel_b = Channel("id13", "channel_test_remove", "channel_admin", channel.Group("group1"), ["toi"])
        channel_b.remove_member("toi")
        self.assertEqual(channel_b.channel_members, ["channel_admin"])
        channel_b.remove_member("channel_admin")
        self.assertEqual(channel_b.channel_members, [])
        with self.assertRaises(channel.ParamNotFoundException):
            channel_b.remove_member("toto")



if __name__ == '__main__':
    unittest.main()
