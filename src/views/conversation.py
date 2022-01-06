#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente une zone de conversation.
"""
import json
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView

from src.config import config
from src.libs.bot.commands import Commands
from src.models.message import Message
from src.models.mongo_connector import MongoConnector

Builder.load_file("{0}/conversation.kv".format(config.VIEWS_DIR))


class InputsContainer(BoxLayout):
    pass


class MessageLabel(Label):
    pass


class MessageSent(MessageLabel):
    pass


class MessageReceived(MessageLabel):
    pass


class ConversationContainer(ScrollView):

    def __init__(self, channel_id):
        super(ConversationContainer, self).__init__()
        self.channel_id = channel_id
        self.messages_box = self.ids.messages_container

        # Démarrer la mise à jour régulière de la conversation
        self.constant_update(channel_id)

    def constant_update(self, channel_id):
        self.init_conversation(channel_id)
        # time.sleep(1)

    def init_conversation(self, channel_id):
        try:
            with MongoConnector() as connector:
                collection = connector.db["messages"].find()
                for document in collection:
                    if document['channel_id'] == channel_id:
                        msg = MessageSent(
                            text=document["timestamp"] + " - " + document["sender"] + "\n" + document["msg"])
                        self.messages_box.add_widget(msg, len(self.messages_box.children))
        except Exception as e:
            print(e)

        # conv_file_path = config.PUBLIC_DIR + "/tmp_conversations/basic.json"
        # with open(conv_file_path) as json_file:
        #    conv = json.load(json_file)

        # for message in conv["data"]:
        #    msg = MessageSent(text=message["timestamp"] + " - " + message["sender"] + "\n" + message["msg"])
        #    self.messages_box.add_widget(msg, len(self.messages_box.children))

    def add_message(self, msg_obj, pos="left"):
        msg = MessageSent()

        if pos == "right":
            msg = MessageReceived()  # ici
        msg.text = str(msg_obj.timestamp) + " - " + msg_obj.sender + "\n" + msg_obj.msg
        self.messages_box.add_widget(msg, len(self.messages_box.children))


class Conversation(RelativeLayout):
    def __init__(self, channel):
        super(Conversation, self).__init__()
        print(channel.channel_id)
        self.messages_container = ConversationContainer(channel.channel_id)
        # self.messages_container = ConversationContainer(channel._id)
        self.inputs_container = InputsContainer()

        self.add_widget(self.messages_container)
        self.add_widget(self.inputs_container)

    def send_message(self):
        txt = self.inputs_container.ids.message_input.text

        if txt:
            msg = Message(datetime.now(), txt, "Moi", self.messages_container.channel_id)
            print(self.messages_container.channel_id)
            if msg.sender == "Moi":  # ici faire en sorte de récuperer l'id de l'user actuel
                self.messages_container.add_message(msg, pos="right")
            else:
                self.messages_container.add_message(msg)
            msg.send_to_db()

            if txt[0] == "/":
                bot = Commands(txt)
                response_from_bot = bot.result
                msg_res = Message(datetime.now(), response_from_bot, "E-Bot")
                self.messages_container.add_message(msg_res, pos="right")

            self.inputs_container.ids.message_input.text = ""
