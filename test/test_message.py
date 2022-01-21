#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.models.message import Message
import unittest
import uuid

class TestMessage(unittest.TestCase):
    def test_init_message(self):
        # test timestamp = int
        with self.assertRaises(TypeError):
            Message(timestamp=123,
                    msg="test",
                    sender="test",
                    is_edited=True,
                    channel_id=None,
                    conversation_id=None,
                    )
        # test msg = int
        with self.assertRaises(TypeError):
            Message(timestamp="test",
                    msg=123,
                    sender="test",
                    is_edited=True,
                    channel_id=None,
                    conversation_id=None,
                    )
        # test sender = int
        with self.assertRaises(TypeError):
            Message(timestamp="test",
                    msg="test",
                    sender=123,
                    is_edited=True,
                    channel_id=None,
                    conversation_id=None,
                    )
        # test is_edited = int
        with self.assertRaises(TypeError):
            Message(timestamp="test",
                    msg="test",
                    sender="test",
                    is_edited=123,
                    channel_id=None,
                    conversation_id=None,
                    )
        # test channel_id = int
        with self.assertRaises(TypeError):
            Message(timestamp="test",
                    msg="test",
                    sender="test",
                    is_edited=True,
                    channel_id=123,
                    conversation_id=None,
                    )
        # test channel_id = int
        with self.assertRaises(TypeError):
            Message(timestamp="test",
                    msg="test",
                    sender="test",
                    is_edited=True,
                    channel_id=None,
                    conversation_id=123,
                    )

    def test_db_formating(self):
        test_dict={'_id': 'test',
                    'timestamp': 'test',
                    'msg': 'test',
                    'sender': 'test',
                    'is_edited': False,
                    'channel_id': "test",
                    'conversation_id': None
                    }
        test_message=Message(timestamp="test",
                            msg="test",
                            sender="test",
                            is_edited=False,
                            channel_id="test",
                            conversation_id=None,
                             )

        self.assertEqual(test_dict['timestamp'], test_message.timestamp)
        self.assertEqual(test_dict['msg'], test_message.msg)
        self.assertEqual(test_dict['sender'], test_message.sender)
        self.assertEqual(test_dict['is_edited'], test_message.is_edited)
        self.assertEqual(test_dict['channel_id'], test_message.channel_id)
        self.assertEqual(test_dict['conversation_id'], test_message.conversation_id)

        test_dict2 = {'_id': 'test2',
                             'timestamp': 'test2',
                             'msg': 'test2',
                             'sender': 'test2',
                             'is_edited': True,
                             'channel_id': None,
                             'conversation_id': "Test2"
                             }

        self.assertNotEqual(test_dict2['timestamp'], test_message.timestamp)
        self.assertNotEqual(test_dict2['msg'], test_message.msg)
        self.assertNotEqual(test_dict2['sender'], test_message.sender)
        self.assertNotEqual(test_dict2['is_edited'], test_message.is_edited)
        self.assertNotEqual(test_dict2['channel_id'], test_message.channel_id)
        self.assertNotEqual(test_dict2['conversation_id'], test_message.conversation_id)

    def test_update_msg(self):
        test_message = Message(timestamp="test",
                               msg="test",
                               sender="test",
                               is_edited=False,
                               channel_id="test",
                               conversation_id=None,
                               )

        new_text="new_test"
        test_message.update_msg(new_text)

        self.assertEqual(test_message.msg, new_text)