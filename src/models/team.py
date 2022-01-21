#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ce fichier contient une classe représentant une équipe.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""

from src.models.channel import Channel
from src.models.mongo_connector import MongoConnector


class Team:
    def __init__(self, identifier: str, name: str, group_names: list, admin_team: list, channels: list,
                 icon_path=None or list,
                 participants=None or list):
        """create a new class object"""
        """
        PRE : identifier and name are strings, group_names, admin_team and channels are lists.
        POST : a new team object is created
        RAISES : if identifier and name  are not str => TypeError
        RAISES : if channels,group_names and admin_team are not list => TypeError
        RAISES : if icon_path and participants  are not str or None => TypeError
        """
        if not isinstance(identifier, str):
            raise TypeError("Invalid arg type : identifier")
        if not isinstance(name, str):
            raise TypeError("Invalid arg type : name")
        if not isinstance(channels, list):
            raise TypeError("Invalid arg type : channels")
        if not isinstance(group_names, list):
            raise TypeError("Invalid arg type : group_names")
        if not isinstance(admin_team, list):
            raise TypeError("Invalid arg type : admin_team")
        if (not isinstance(icon_path, str)) and (icon_path is not None):
            raise TypeError("Invalid arg type : icon_path")
        if not isinstance(participants, list) and participants is not None:
            raise TypeError("Invalid arg type : participants")
        else:
            self.identifier = identifier
            self.name = name
            self.channels = channels
            self.group_names = group_names
            self.participants = participants
            self.admin_team = admin_team
            self.icon_path = icon_path
            try:
                with MongoConnector() as connector:
                    self.__collection = connector.db["teams"]
            except Exception as error:
                print(error)

    def add_channel_to_current_team(self, new_channel: Channel):
        """add a new channel to the team"""
        """
        PRE : new_channel is a Channel Object
        POST : new_channel's id is added to the curent team's list of the channel ids, new_channel is added on db
        RAISES : if new_channel is not Channel => TypeError
        """
        if not isinstance(new_channel, Channel):
            raise TypeError("Invalid arg type : new_channel")
        else:
            # ajout de l'objet Channel dans la liste des channels
            self.channels.append(new_channel)
            # appel de la fonction permettant d'update la collection
            self.add_channel_on_db(new_channel.channel_id)

    def add_channel_on_db(self, channel_id : str):
        """add a channel to the db"""
        """
        PRE : channel_id is a string 
        POST : a new channel is added to the db
        RAISES : if channel_id is not str => TypeError
        """
        if not isinstance(channel_id, str):
            raise TypeError("Invalid arg type : channel_id")
        else:
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

    def add_member(self, member : str):
        """add a new member to the team"""
        """
        PRE : member is a string
        POST : member is added to the list of members of the channel
        RAISES : if member is not str => TypeError
        """
        if not isinstance(member, str):
            raise TypeError("Invalid arg type : member")
        else:
            # ajout du participant dans la liste contenue dans l'objet Team
            self.participants.append(member)
            # update dans la DB
            query = {"name": self.name}
            new_member = {"$set": {
                "participants": self.participants
            }}
            self.__collection.update_one(filter=query, update=new_member)

    def add_group(self, new_group_name : str):
        """add a new group to the team"""
        """
        PRE : member is a string
        POST : member is added to the list of members of the channel
        RAISES : if new_group_name is not Str => TypeError
        """
        if not isinstance(new_group_name, str):
            raise TypeError("Invalid arg type : new_group_name")
        else:
            # ajout du participant dans la liste contenue dans l'objet Team
            self.group_names.append(new_group_name)
            # update dans la DB
            query = {"name": self.name}
            new_group_list = {"$set": {
                "group_names": self.group_names
            }}
            self.__collection.update_one(filter=query, update=new_group_list)

    def is_admin_team(self, member):
        """Check if the user is an admin of the team"""
        """
        PRE : member is a string
        POST : returns a boolean: True if the user is an admin of the team, else false
        RAISES : if member is not str => TypeError
        """
        if not isinstance(member, str):
            raise TypeError("Invalid arg type : member")
        else:
            is_admin = False
            for i in self.admin_team:
                if member == i:
                    is_admin = True
            return is_admin

    def is_member_team(self, member):
        """Check if the user is a mamber of the team"""
        """
        PRE : member is a string
        POST : returns a boolean: True if the user is a member of the team, else false
        RAISES : if member is not str => TypeError
        """
        if not isinstance(member, str):
            raise TypeError("Invalid arg type : member")
        else:
            is_member = False
            for i in self.participants:
                if member == i:
                    is_member = True
            return is_member

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
