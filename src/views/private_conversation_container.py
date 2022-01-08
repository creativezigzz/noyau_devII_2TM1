#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManagerException
from kivy.uix.scrollview import ScrollView

from main import Main
from src.config import config
from src.models.mongo_connector import MongoConnector
from src.models.private_conversation import PrivateConversation
from src.models.screens_manager import ScreensManager

#Builder.load_file("{0}/conversation.kv".format(config.VIEWS_DIR))


class ConversationListButton(Button):
    pass


class PrivateConversationContainer(ScrollView):
    def __init__(self):
        super(PrivateConversationContainer, self).__init__()
        self.content = self.ids.conversation_content
        self.curren_user = Main.current_user
        self.conversation_list = []
        self.get_conversation_from_db()
        self.sm = ScreensManager()
        self.landing_screen = self.get_landing_screen()

    def get_landing_screen(self):
        """Recuperation du landing_screen"""
        """
        POST : return landing_screen
        """
        try:
            landing_screen = self.sm.get_screen("landing")
            return landing_screen
        except ScreenManagerException:
            return None

    def get_conversation_from_db(self):
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
        self.content.clear_widgets()
        for conversation in self.conversation_list:
            conversation_name_row = ConversationListButton(text=conversation.name,
                                                           on_press=lambda a, _conversation_unit=conversation:
                                                           self.display_landing_screen(_conversation_unit)
                                                           )
            self.content.add_widget(conversation_name_row)

    def display_landing_screen(self, conversation):
        """display the member-box and the messages-box"""
        """
        PRE : membres is list of strings, channel is Channel, team and id_channel are string
        """
        print(conversation)
        self.landing_screen.display_participant_conversation(conversation)
        self.landing_screen.display_conversation(channel=None, private_conversation=conversation)
