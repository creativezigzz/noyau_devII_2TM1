#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente une vue contenant la liste des "Team" disponible à l'utilisateur.
"""
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManagerException
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from main import Main
from src.config import config
from src.libs.sorting.dict_sort import dict_sort
from src.models.channel import Channel
from src.models.group import Group
from src.models.mongo_connector import MongoConnector
from src.models.screens_manager import ScreensManager
from src.models.team import Team

Builder.load_file("{0}/teams.kv".format(config.VIEWS_DIR))


class TeamsListButton(Button):
    pass


class EmptyTeams(Label):
    pass


class TeamsContainer(ScrollView):

    def __init__(self):
        super(TeamsContainer, self).__init__()
        self.content = self.ids.channels_content
        self.sm = ScreensManager()
        self.data_from_db = {}
        self.set_data_from_db()
        self.init_teams_list()

    def set_data_from_db(self):

        try:
            with MongoConnector() as connector:
                collection = connector.db["teams"]
                for document in collection.find():

                    self.data_from_db[document["_id"]] = {
                        "name": document["name"],
                        "icon_path": "",
                        "group_names": document["group_names"],
                        "admin_team": document["admin_team"],
                        "participants": document["participants"],
                        "channels": []
                    }
                    collection_channels = connector.db["channels"]
                    for channel in collection_channels.find():
                        for i in document["channel_id"]:
                            # print(str(channel["channel_id"])+ " =? "+ str(i))
                            if channel["channel_id"] == i:
                                data = Channel(

                                    channel_id=channel["channel_id"],
                                    channel_name=channel["name"],
                                    channel_admin=channel["admin"],
                                    group=Group(name=channel["group"]),
                                    channel_members=channel["membres"],
                                    chat_history=None
                                )

                                # print(str(data))
                                # print(data.channel_id)
                                self.data_from_db[document["_id"]]["channels"].append(data)

        except Exception as e:
            print(e)

        # print(self.data_from_db)

    def init_teams_list(self):
        """
            [BASE]
            Initialise la liste des "Team" auxquelles l'utilisateur est inscrit.
            Si l'utilisateur fait partie de channels, il est affiché dans la liste des membres dans le container concerné.
            Sinon, un message s'affiche précisant que l'utilisateur ne fait partie d'aucun channel.
        """
        self.content.clear_widgets()
        teams_list = self.get_teams_list()
        private_conversation = TeamsListButton(text="privé")
        private_conversation.bind(
            on_press=lambda a: self.display_landing_screen_private_conversation())
        self.content.add_widget(private_conversation)
        if teams_list:
            for team in teams_list:
                channel_label = TeamsListButton(text=team.name)
                channel_label.bind(
                    on_press=lambda a, _channels=team.channels, _team=team: self.display_landing_screen_team(_channels,
                                                                                                             _team))
                self.content.add_widget(channel_label)
            button_add_team = TeamsListButton(text="Ajouter")
            button_add_team.bind(
                on_press=lambda a: self.add_team())

            self.content.add_widget(button_add_team)
        else:
            self.content.add_widget(EmptyTeams())

    def display_landing_screen_team(self, channels, team: Team):
        try:
            landing_screen = self.sm.get_screen("landing")
        except ScreenManagerException:
            landing_screen = None
        landing_screen.display_channels(channels, team)
        landing_screen.display_participant_team(team)

    def display_landing_screen_private_conversation(self):
        try:
            landing_screen = self.sm.get_screen("landing")
        except ScreenManagerException:
            landing_screen = None
        landing_screen.display_private_conversation()

    def get_teams_list(self):
        """
            [BASE]
            Récupère la liste des "Team" depuis la banque de données.
            :return : list : La liste des "Team" (objets) auxquels l'utilisateur appartient, triés par nom.
        """

        list_of_teams = []

        if self.data_from_db:

            # Trier sur le nom grâce à notre librairie de tri src.libs.sorting
            data_from_db = dict_sort(self.data_from_db, "name")

            for team_id in data_from_db:
                name = data_from_db[team_id]["name"]
                icon_path = data_from_db[team_id]["icon_path"]
                participants = data_from_db[team_id]["participants"]
                group_names = data_from_db[team_id]["group_names"]
                admin_team = data_from_db[team_id]["admin_team"]
                channels = data_from_db[team_id]["channels"]
                inst = Team(identifier=str(team_id),
                            name=name,
                            channels=channels,
                            group_names=group_names,
                            admin_team=admin_team,
                            icon_path=icon_path,
                            participants=participants)
                if inst.is_member_team(Main.current_user):
                    list_of_teams.append(inst)
            return list_of_teams

        return None

    def add_team(self):

        # content est tout le popup
        content_popup_team = RelativeLayout()
        team_name_input = TextInput(text='', font_size=14, size_hint_y=None, height=50,
                                    pos_hint={'center_x': .5, 'center_y': .3})

        close = Button(text="Close", size_hint=(None, None), size=(150, 40),
                       pos_hint={'center_x': .6, 'center_y': .1})

        ajouter = Button(text="Ajouter", size_hint=(None, None), size=(150, 40),
                         pos_hint={'center_x': .4, 'center_y': .1})
        # ajout des button, de l'input et du label au popup
        content_popup_team.add_widget(Label(text="Le nom de la nouvelle team"))
        content_popup_team.add_widget(team_name_input)
        content_popup_team.add_widget(ajouter)
        content_popup_team.add_widget(close)
        popup = Popup(title="Ajouter une nouvelle team ",
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      content=content_popup_team,
                      auto_dismiss=False)

        # définition des actions liée au button
        close.bind(on_press=lambda a: popup.dismiss())
        ajouter.bind(on_press=lambda a: self.add_team_on_db(team_name_input.text, popup))
        popup.open()

    def add_team_on_db(self, team_name: str, popup):
        """
        Ajoute une nouvelle team dans la collection "teams" de la db dont le seul participant est le current_user
        """
        new_team = {
            "name": team_name,
            "icon_path": "",
            "admin_team": [Main.current_user],
            "participants": [Main.current_user],
            "channel_id": []
        }
        try:
            with MongoConnector() as connector:
                db = connector.db
                collection_team = db["teams"]
                collection_team.insert_one(new_team)
        except Exception as e:
            print(e)
        self.set_data_from_db()
        self.init_teams_list()
        popup.dismiss()
