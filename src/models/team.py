#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ce fichier contient une classe représentant une équipe.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""
from src.models.mongo_connector import MongoConnector


class Team:
    def __init__(self, identifier, name, channels, icon_path=None, participants=None):
        self.identifier = identifier
        self.name = name
        self.channels = channels
        self.icon_path = icon_path
        self.participants = participants

        try:
            with MongoConnector() as connector:
                self.__collection = connector.db["teams"]
        except Exception as error:
            print(error)

    def join(self):
        """
            Méthode permettant à un utilisateur de rejoindre cette équipe.
        """
        pass

    def leave(self):
        """
            Méthode permettant à un utilisateur de quitter cette équipe.
        """
        pass

    def get_participants_status(self):
        pass

    def add_member(self, member):
        """add a new member to the channel"""
        """
        PRE : member is a string
        POST : member is added to the list of members of the channel
        """
        self.participants.append(member)
        query = {"name": self.name}
        new_member = {"$set": {
            "participants": self.participants
        }}
        self.__collection.update_one(filter=query, update=new_member)
