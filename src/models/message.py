#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ce fichier contient une classe représentant un message textuel envoyé dans un channel.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""

import traceback


from src.models.mongo_connector import MongoConnector
import uuid


# pour l'auto increment

class Message:

    def __init__(self, timestamp, msg, sender, channel_id, conversation_id, is_edited=False):
        """create a new Message object"""
        """
        PRE : timestamp is a datetime object, msg, sender and channel_id are string
        POST : a new message object is created 
        """
        self.timestamp = timestamp
        self.msg = msg
        self.sender = sender
        self.is_edited = is_edited
        self._id = uuid.uuid4()
        self.channel_id = channel_id
        self.conversation_id = conversation_id

        try:
            with MongoConnector() as connector:
                self.__collection = connector.db["messages"]
        except Exception as e:
            print(e)

    def db_formatting(self):
        """return the message object in the db format"""
        """
        PRE : 
        POST : return a dict: the message object in the db format
        """
        return {
            "_id": self._id,
            "timestamp": str(self.timestamp),
            "msg": self.msg,
            "sender": self.sender,
            "is_edited": self.is_edited,
            "channel_id": self.channel_id,
            "conversation_id": str(self.conversation_id)
        }

    def send_to_db(self):
        """send the message object to db"""
        """
        PRE : 
        POST : the message is sent to the db
        """
        self.__collection.insert_one(self.db_formatting())

    def update_msg(self, new_msg):
        """ubdate the message object (self.msg)"""
        """
        PRE : new_msg is a string
        POST : self.msg is replaced by new_message
        """
        self.__collection.find_one_and_update(self._id, {'msg': new_msg})

    def delete_db(self):
        """delete the message object"""
        """
        PRE : 
        POST : the message is deleted of the db
        """
        self.__collection.delete_one(self._id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb)
        return True
