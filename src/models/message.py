#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ce fichier contient une classe représentant un message textuel envoyé dans un channel.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""
import json

from src.config import config
from src.models.mongo_connector import MongoConnector


class Message:
    def __init__(self, msg_id, timestamp, msg, sender, channel_id, is_edited=False):
        self.timestamp = timestamp
        self.msg = msg
        self.sender = sender
        self.channel_id = channel_id
        self.is_edited = is_edited
        self.msg_id = msg_id

        try:
            with MongoConnector() as connector:
                self.__collection = connector.db["messages"]
        except Exception as e:
            print(e)

    def db_formatting(self):
        return {
            "timestamp": str(self.timestamp),
            "msg": self.msg,
            "sender": self.sender,
            "channel_id": self.channel_id,
            "is_edited": self.is_edited,
            "msg_id": self.msg_id
        }

    def send_to_db(self):
        # conv_file_path = config.PUBLIC_DIR + "/tmp_conversations/basic.json"
        # with open(conv_file_path) as json_file:
        #     conv = json.load(json_file)
        #
        # conv["data"].append(self.db_formatting())
        #
        # with open(conv_file_path, 'w') as outfile:
        #     json.dump(conv, outfile)
        self.__collection.insert_one(self.db_formatting())

    def update_msg(self, new_msg):

        self.__collection.find_one_and_update(self.msg_id, {'msg': new_msg})

    def delete_db(self):
        self.__collection.delete_one(self.msg_id)

