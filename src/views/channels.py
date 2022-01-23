#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente la liste des 'Channel' disponibles pour l'utilisateur.
"""
import uuid

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManagerException
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from main import Main
from src.config import config
from src.models.channel import Channel
from src.models.group import Group
from src.models.screens_manager import ScreensManager
from src.models.team import Team

Builder.load_file("{0}/channel.kv".format(config.VIEWS_DIR))


class GroupTitleRow(BoxLayout):
    pass


class GroupLabel(Label):
    pass


class GroupAddButton(Button):
    pass


class ChannelsListButton(Button):
    pass


class MembersListButton(Button):
    pass


class ChannelsContainer(ScrollView):
    def __init__(self, channels_list_obj: list, team: Team):
        """initialisation of the ChannelContainer"""
        """
        PRE : membres is list of strings, channel is Channel, team and id_channel are string
        POST : channelsContainer is initialised
        """
        super(ChannelsContainer, self).__init__()
        self.channels_list = channels_list_obj
        self.team_object = team
        self.channels_container = self.ids.channels_content
        self.sm = ScreensManager()
        self.landing_screen = self.get_landing_screen()
        self.generate_list_rows()

    def get_landing_screen(self):
        """Recovery of the landing_screen"""
        """
        PRE : -
        POST : return landing_screen
        """
        try:
            landing_screen = self.sm.get_screen("landing")
            return landing_screen
        except ScreenManagerException:
            return None

    def generate_list_rows(self):
        """generate the list of groups and channels"""
        """
        PRE : 
        POST : the list is generated
        """
        self.channels_container.clear_widgets()
        groups = {}
        for channel in self.channels_list:
            group_name = channel.group.name
            if group_name not in groups:
                group = BoxLayout(orientation="vertical", size_hint_y=None)
                title_row = GroupTitleRow()
                title_label = GroupLabel(text=group_name)
                title_add_btn = GroupAddButton(on_press=lambda a, _grp=group_name: self.add_new_channel(_grp))
                title_row.add_widget(title_label)
                title_row.add_widget(title_add_btn)
                group.add_widget(title_row)
                self.channels_container.add_widget(group)
                groups[channel.group.name] = group
            channel_name_row = ChannelsListButton(text=channel.channel_name,
                                                  on_press=lambda a, _membres=channel.channel_members, _channel=channel:
                                                  self.display_landing_screen(_membres, _channel, self.team_object)
                                                  )
            groups[group_name].add_widget(channel_name_row)
        # vérification de si il existe des groupes sans channels
        for group_name in self.team_object.group_names:
            if group_name not in groups:
                group = BoxLayout(orientation="vertical", size_hint_y=None)
                title_row = GroupTitleRow()
                title_label = GroupLabel(text=group_name)
                title_add_btn = GroupAddButton(on_press=lambda a, _grp=group_name: self.add_new_channel(_grp))
                title_row.add_widget(title_label)
                title_row.add_widget(title_add_btn)
                group.add_widget(title_row)
                self.channels_container.add_widget(group)
                groups[group_name] = group
        # Ajout de la possibilité d'ajouter un groupe si on est admin de la team
        if self.team_object.is_admin_team(Main.current_user):
            group_add = BoxLayout(orientation="vertical", size_hint_y=None)
            title_row = GroupTitleRow()
            title_label = GroupLabel(text="new groupe")
            title_add_btn = GroupAddButton(on_press=lambda a: self.add_new_group())
            title_row.add_widget(title_label)
            title_row.add_widget(title_add_btn)
            group_add.add_widget(title_row)
            self.channels_container.add_widget(group_add)

    def display_landing_screen(self, membres, channel, team):
        """display the member-box and the messages-box"""
        """
        PRE : membres is list of strings, channel is Channel, team and id_channel are string
        """
        self.landing_screen.display_participant_channel(membres, channel, team)
        self.landing_screen.display_conversation(channel=channel, private_conversation=None)

    def add_new_group(self):
        """add a new group to the channel"""
        """
        PRE : -
        POST : the new group is added
        """
        print("nouveau groupe")
        content = RelativeLayout()
        group_name_input = TextInput(text='', font_size=14, size_hint_y=None, height=50,
                                     pos_hint={'center_x': .5, 'center_y': .3})

        cancel = Button(text="Annuler", size_hint=(None, None), size=(150, 40),
                        pos_hint={'center_x': .6, 'center_y': .1})

        ajouter = Button(text="Ajouter", size_hint=(None, None), size=(150, 40),
                         pos_hint={'center_x': .4, 'center_y': .1})
        # ajout des button, de l'input et du label a la popup
        content.add_widget(Label(text="Le nom du nouveau group"))
        content.add_widget(group_name_input)
        content.add_widget(ajouter)
        content.add_widget(cancel)
        popup = Popup(title="Ajouter un nouveau groupe à la team {0}".format(self.team_object.name),
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      content=content,
                      auto_dismiss=False)

        # définition des actions liée au button
        cancel.bind(on_press=lambda a: popup.dismiss())
        ajouter.bind(
            on_press=lambda a: self.add_new_group_on_db(group_name_input.text) and popup.dismiss())
        popup.open()

    def add_new_channel(self, group_name):
        """add a new channel identified by the group 'group_name'"""
        """
        PRE : group_name is a string
        POST : the new channel is added
        """
        # content est toute la popup
        content = RelativeLayout()
        channel_name_input = TextInput(text='', font_size=14, size_hint_y=None, height=50,
                                       pos_hint={'center_x': .5, 'center_y': .3})

        cancel = Button(text="Annuler", size_hint=(None, None), size=(150, 40),
                        pos_hint={'center_x': .6, 'center_y': .1})

        ajouter = Button(text="Ajouter", size_hint=(None, None), size=(150, 40),
                         pos_hint={'center_x': .4, 'center_y': .1})
        # ajout des button, de l'input et du label a la popup
        content.add_widget(Label(text="Le nom du nouveau channel et d'autres éléments"))
        content.add_widget(channel_name_input)
        content.add_widget(ajouter)
        content.add_widget(cancel)
        popup = Popup(title="Ajouter un nouveau channel à {0}".format(group_name),
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      content=content,
                      auto_dismiss=False)
        team = self.team_object

        # définition des actions liée au button
        cancel.bind(on_press=lambda a: popup.dismiss())
        ajouter.bind(on_press=lambda a: self.add_new_channel_on_db(channel_name_input.text, group_name,
                                                                   team) and popup.dismiss())
        popup.open()

    def add_new_channel_on_db(self, channel_name, group_name, team: Team):
        """create a new channel into the Db (into channel collection and into team collection) """
        """
        PRE : team is an Team object , channel is an Channel object
        """
        new_channel = Channel(

            channel_id=str(uuid.uuid4()),
            channel_name=channel_name,
            channel_admin="Admin_test",
            group=Group(name=group_name),
            channel_members=[]
        )
        new_channel.send_to_db()
        team.add_channel_to_current_team(new_channel)
        self.generate_list_rows()

    def add_new_group_on_db(self, new_group_name: str):
        """create a new channel into the Db (into channel collection and into team collection) """
        """
        PRE : team is an Team object , channel is an Channel object
        """
        print(new_group_name)
        self.team_object.add_group(new_group_name)
        self.generate_list_rows()


class ParticipantContainer(ScrollView):
    def __init__(self, member_list, channel, team, conversation,
                 display_team_member: bool, display_channels_member: bool):
        """create the container who contains all the user in the current channel"""
        """
        PRE : member_list is list, channel is Channel object, team is strings
        """
        super(ParticipantContainer, self).__init__()
        self.display_team_member = display_team_member
        self.display_channels_member = display_channels_member
        self.content = self.ids.member_content
        self.membres_list = member_list
        self.channel = channel
        self.team = team
        self.conversation = conversation
        self.init_member_list()
        self.sm = ScreensManager()
        self.landing_screen = self.get_landing_screen()

    def get_landing_screen(self):
        """get the landing screen"""
        """
        POST : return the landing_screen
        """
        try:
            landing_screen = self.sm.get_screen("landing")
            return landing_screen
        except ScreenManagerException:
            return None

    def init_member_list(self):
        """set the member list of the current channel"""
        self.content.clear_widgets()
        for member in self.membres_list:
            member_label = MembersListButton(text=member)
            if member in Main.current_user_logged:
                member_label.color = (0, 255, 0, 1)
            member_label.size_hint_y = 0.1
            member_label.size_hint_max_y = 20
            self.content.add_widget(member_label)
        add_button_label = MembersListButton(text="Ajouter")
        self.content.add_widget(add_button_label)
        add_button_label.size_hint_y = 0.1
        add_button_label.size_hint_max_y = 20
        if self.display_channels_member:
            add_button_label.bind(on_press=lambda a: self.add_member_to_channel("test"))
        if self.display_team_member:
            add_button_label.bind(on_press=lambda a: self.add_member_to_team("test"))
        # !! a faire !!
        else:
            add_button_label.bind(on_press=lambda a: print("ajouter un membre a la conv privé"))

    def add_member_to_channel(self, member_pseudo: str):
        """add a new membre in the channel and update data on DB"""
        """
        PRE : member_pseudo is string , channel is Channel object
        """
        self.channel.add_member(member_pseudo)
        self.init_member_list()

    def add_member_to_team(self, member_pseudo: str):
        """add a new membre in the channel and update data on DB"""
        """
        PRE : member_pseudo is string , channel is Channel object
        """
        self.team.add_member(member_pseudo)
        self.init_member_list()
