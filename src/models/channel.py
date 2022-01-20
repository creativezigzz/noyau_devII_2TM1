#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
import uuid

from src.models.group import Group

"""
    Ce fichier contient une classe représentant un channel.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""

from src.models.mongo_connector import MongoConnector


class ParamNotFoundException(Exception):
    pass


class WrongTypeException(Exception):
    pass


class Channel:
    """class to create a new channel, it can add and remove members to this channel"""

    def __init__(self, channel_id: str, channel_name: str, channel_admin: str, group: Group,
                 channel_members: list,
                 chat_history=None):
        """create a new channel based on a name, an administrator, some members and a chat history"""
        """
        PRE : channel_name,channel_id and channel_admin are strings,
                group is Group,
                channel_members and chat_history are lists of strings
        POST : a new Channel object is created
        RAISE : AssertionError if the parameter are not of the good types.
        """
        if chat_history is None:
            chat_history = []
        self._id = uuid.uuid4()
        assert isinstance(channel_id, str)
        self.channel_id = channel_id
        assert isinstance(channel_name, str)
        self.channel_name = channel_name
        assert isinstance(channel_admin, str)
        self.channel_admin = channel_admin
        assert isinstance(group, Group)
        self.group = group

        assert isinstance(channel_members, list)
        for member in channel_members:
            assert isinstance(member, str)
        self.channel_members = channel_members  # pour moi channel_members serait une
        # liste de string (comme ça on peut ajouter et supprimer des membres facilement
        # ajout automatique de l'admin dans la liste des membres
        self.channel_members.append(self.channel_admin)
        assert isinstance(chat_history, list)
        self.chat_history = chat_history  # même chose que pour channel_members

        try:
            with MongoConnector() as connector:
                self.__collection = connector.db["channels"]

        except Exception as error:
            print(error)

    def send_to_db(self):
        """send the channel to the database"""
        """
        PRE : 
        POST : the channel is sent to the database
        """
        query = {
            "channel_id": self.channel_id,
            "name": self.channel_name,
            "admin": self.channel_admin,
            "group": self.group.name,
            "membres": self.channel_members,
            # "chat_history": self.chat_history
        }
        self.__collection.insert_one(query)
        # verification en console
        try:
            with MongoConnector() as connector:
                for x in connector.db["channels"].find():
                    print(x)
        except Exception as e:
            print(e)

    def add_member(self, member):
        """add a new member to the channel"""
        """
        PRE : member is a string
        POST : member is added to the list of members of the channel
        RAISE : WrongTypeException if the member parameter is not a string 
        """
        if type(member) != str:
            raise WrongTypeException("please enter a string !")
        self.channel_members.append(member)
        query = {"channel_id": self.channel_id}
        new_member = {"$set": {
            "membres": self.channel_members
        }}
        self.__collection.update_one(filter=query, update=new_member)

    def remove_member(self, member):
        """remove a member from the channel, it removes all the members that have the pseudo member"""
        """
        PRE : member is a string that is in the list channel_members
        POST : all the element 'member' of the list channel_members are removed
        RAISE : ParamNotFoundException if member is not in channel_members, WrongTypeException if member is not a string
        """
        if type(member) != str:
            raise WrongTypeException("please enter a string !")
        if member not in self.channel_members:
            raise ParamNotFoundException(Exception)
        self.channel_members = [i for i in self.channel_members if i != member]  # permet de supprimer chaque élément
        # member de la liste (même s'il revient plusieurs fois), remove ne supprime que la premiere occurrence
        query = {"channel_name": self.channel_name}
        member_to_remove = {"$set": {
            "channel_members": self.channel_members
        }}
        self.__collection.update_one(query, member_to_remove)

    def mute_group(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb)
        return True
