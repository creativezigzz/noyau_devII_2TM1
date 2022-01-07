#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ce fichier contient une classe représentant une équipe.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""
from src.models.channel import Channel
from src.models.mongo_connector import MongoConnector


class Team:
    def __init__(self, identifier: str, name: str, group_names: list, admin_team: list, channels: list, icon_path=None,
                 participants=None):
        """create a new class object"""
        """
        PRE : identifier and name are strings, group_names, admin_team and channels are lists.
        POST : a new team object is created
        """
        self.identifier = identifier
        self.name = name
        self.channels = channels
        self.group_names = group_names
        self.admin_team = admin_team
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
        PRE : new_channel is a Channel Object
        POST : new_channel's id is added to the list of the channel ids, new_channel is added on db
        """
        # ajout de l'objet Channel dans la liste des channels
        self.channels.append(new_channel)
        # appel de la fonction permettant d'update la collection
        self.add_channel_on_db(new_channel.channel_id)

    def add_channel_on_db(self, channel_id):
        """add a channel to the db"""
        """
        PRE : channel_id is a string (the id of a channel object)
        POST : a new channel is added to the db
        """
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

    def add_group(self, new_group_name):
        """add a new group to the team"""
        """
        PRE : member is a string
        POST : member is added to the list of members of the channel
        """
        # ajout du participant dans la liste contenue dans l'objet Team
        self.group_names.append(new_group_name)
        # update dans la DB
        query = {"name": self.name}
        new_group_list = {"$set": {
            "group_names": self.group_names
        }}
        self.__collection.update_one(filter=query, update=new_group_list)

    def is_admin_team(self, membre):
        """Check if the user is an admin of the team"""
        """
        PRE : membre is a string
        POST : return a boolean: True if the user is an admin of the team, else false
        """
        is_admin = False
        for i in self.admin_team:
            if membre == i:
                is_admin = True
        return is_admin

    def is_member_team(self, membre):
        """Check if the user is a mamber of the team"""
        """
        PRE : membre is a string
        POST : return a boolean: True if the user is a member of the team, else false
        """
        is_member = False
        for i in self.participants:
            if membre == i:
                is_member = True
        return is_member
