#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from src.models.mongo_connector import MongoConnector
from src.models.private_conversation import PrivateConversation
from src.models.screens_manager import ScreensManager


class ConversationListButton(Button):
    pass


class ConversationAddButton(Button):
    pass


class PrivateConversationContainer(ScrollView):
    def __init__(self):
        """init the conversation container for private conversations"""
        super(PrivateConversationContainer, self).__init__()
        self.content = self.ids.conversation_content
        self.curren_user = Main.current_user
        self.conversation_list = []
        self.get_conversation_from_db()
        self.sm = ScreensManager()
        self.landing_screen = self.get_landing_screen()

    def get_landing_screen(self):
        """Recovery of the landing_screen"""
        """
        POST : return landing_screen
        """
        try:
            landing_screen = self.sm.get_screen("landing")
            return landing_screen
        except ScreenManagerException:
            return None

    def get_conversation_from_db(self):
        """init the conversation from the db"""
        """
        POST : the conversation is initialised
        """
        try:
            with MongoConnector() as connector:
                collection = connector.db["private_messages"]
                for i in collection.find():
                    if self.curren_user in i["members"]:
                        conversation = PrivateConversation(
                            id=i["_id"],
                            name=i["name"],
                            members=i["members"],
                            last_message=i["last_message"]
                        )
                        self.conversation_list.append(conversation)
        except Exception as error:
            print(error)
        for u in self.conversation_list:
            print(u)
            for t in u.messages:
                print(t)
        self.init_conversation_list()

    def init_conversation_list(self):
        """init the conversations in the conversation_list"""
        self.content.clear_widgets()
        for conversation in self.conversation_list:
            conversation_name_row = ConversationListButton(text=conversation.name,
                                                           on_press=lambda a, _conversation_unit=conversation:
                                                           self.display_landing_screen(_conversation_unit)
                                                           )
            self.content.add_widget(conversation_name_row)
        conversation_add = ConversationAddButton(text="Ajouter",
                                                 on_press=lambda a: self.add_new_conversation()
                                                 )
        self.content.add_widget(conversation_add)

    def display_landing_screen(self, conversation):
        """display the member-box and the messages-box"""
        """
        PRE : membres is list of strings, channel is Channel, team and id_channel are string
        """
        print(conversation)
        self.landing_screen.display_participant_conversation(conversation)
        self.landing_screen.display_conversation(channel=None, private_conversation=conversation)

    def create_new_conversation(self, name, members, popup):
        """create a new conversation"""
        """
        PRE : name is a str, members is a list of strings, popup is a Popup object
        POST : a new private conversation is created
        """
        print("ajouter une conversation")
        print(name)
        print(members)
        new_conversation = PrivateConversation(id=None, name=name, members=members, last_message=None)
        print(new_conversation.name)
        print(new_conversation.members)
        print(new_conversation.identifier)
        new_conversation.send_conversation_on_db()
        self.conversation_list.append(new_conversation)
        self.init_conversation_list()
        popup.dismiss()

    def add_new_conversation(self):
        """create the Popup to create a new conversation with create_new_conversation"""
        member = [Main.current_user]
        # content est toute la popup
        content = RelativeLayout()
        conversation_name_input = TextInput(text='', font_size=14, size_hint_y=None, height=50,
                                            pos_hint={'center_x': .5, 'center_y': .3})
        conversation_members = "a faire en dropdown"
        cancel = Button(text="Annuler", size_hint=(None, None), size=(150, 40),
                        pos_hint={'center_x': .6, 'center_y': .1})

        ajouter = Button(text="Ajouter", size_hint=(None, None), size=(150, 40),
                         pos_hint={'center_x': .4, 'center_y': .1})
        # ajout des button, de l'input et du label a la popup
        content.add_widget(Label(text="Le nom de la nouvelle discussion et le/ les membres a ajouter"))
        content.add_widget(conversation_name_input)
        # content.add_widget(conversation_members)
        content.add_widget(ajouter)
        content.add_widget(cancel)
        popup = Popup(title="Créer une nouvelle discussion privée",
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      content=content,
                      auto_dismiss=False)

        # définition des actions liée au button
        cancel.bind(
            on_press=lambda a: popup.dismiss())
        ajouter.bind(
            on_press=lambda a: self.create_new_conversation(conversation_name_input.text, member, popup))
        popup.open()
