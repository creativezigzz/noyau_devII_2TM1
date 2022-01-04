#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ce fichier contient une classe représentant une équipe.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""
from src.models.channel import Channel
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

    def add_channel_to_current_team(self, new_channel: Channel):
        """add a new channel to the team"""
        """
        PRE : new_channel is an Channel Object
        POST : new_channel's id is added to the list of the channel ids
        """
        # ajout de l'objet Channel dans la liste des channels
        self.channels.append(new_channel)
        # appel de la fonction permettant d'update la collection
        self.add_channel_on_db(new_channel.channel_id)

    def add_channel_on_db(self, channel_id):
        # construction d'une nouvelle liste d'id_channel
        new_channel_list = []
        for i in self.channels:
            new_channel_list.append(i.channel_id)
        # ajout de l'id du nouveau channel dans la liste
        new_channel_list.append(channel_id)
        # update dans la DB
        query = {"_id": self.identifier}
        new_member = {"$set": {
            "channel_id": new_channel_list
        }}
        self.__collection.update_one(filter=query, update=new_member)

    def add_member(self, member):
        """add a new member to the team"""
        """
        PRE : member is a string
        POST : member is added to the list of members of the channel
        """
        # ajout du participant dans la liste contenue dans l'objet Team
        self.participants.append(member)
        # update dans la DB
        query = {"name": self.name}
        new_member = {"$set": {
            "participants": self.participants
        }}
        self.__collection.update_one(filter=query, update=new_member)
