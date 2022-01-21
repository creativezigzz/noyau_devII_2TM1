#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente une zone de conversation.
"""
from datetime import datetime
from main import Main

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
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


class MessageSentButton(Button):
    pass


class MessageReceived(MessageLabel):
    pass


class ConversationContainer(ScrollView):

    def __init__(self, channel_id, private_conversation):
        super(ConversationContainer, self).__init__()
        self.channel_id = channel_id
        self.private_conversation = private_conversation
        self.messages_box = self.ids.messages_container

        # Démarrer la mise à jour régulière de la conversation
        self.constant_update()

    def constant_update(self):
        if self.private_conversation is None:
            self.init_conversation_channels(self.channel_id)
        if self.channel_id is None:
            self.init_conversation_private(self.private_conversation)
        # time.sleep(1)

    def init_conversation_channels(self, channel_id):
        try:
            with MongoConnector() as connector:
                collection = connector.db["messages"].find()
                for document in collection:
                    if document['channel_id'] is not None and document['channel_id'] == channel_id:
                        if document["sender"] == Main.current_user:
                            msg = MessageSent(
                                text=document["timestamp"] + " - " + document["sender"] + "\n" + "[ref='click']" +
                                     document["msg"] + "[/ref]", markup=True,
                                on_ref_press=lambda a, _message="Coucou": print(_message))
                            msg_id = document['_id']
                            edit_btn = MessageSentButton(text="edit",
                                                         on_press=lambda a, _msg=msg_id: self.edit_msg(_msg, connector.db["messages"])
                                                         , size_hint=(None, None), size=(50, 40), markup=True)
                            self.messages_box.add_widget(msg)
                            self.messages_box.add_widget(edit_btn)
                        else:
                            msg = MessageReceived(
                                text=document["timestamp"] + " - " + document["sender"] + "\n" +
                                     document["msg"])

                            self.messages_box.add_widget(msg, len(self.messages_box.children))
        except Exception as e:
            print(e)

    def edit_msg(self, msg, collection):
        content = RelativeLayout()
        msg_input = TextInput(text='', font_size=14, size_hint_y=None, height=50,
                                       pos_hint={'center_x': .5, 'center_y': .3})

        cancel = Button(text="Annuler", size_hint=(None, None), size=(150, 40),
                        pos_hint={'center_x': .6, 'center_y': .1})

        update = Button(text="Update", size_hint=(None, None), size=(150, 40),
                         pos_hint={'center_x': .4, 'center_y': .1})
        # ajout des button, de l'input et du label a la popup
        content.add_widget(Label(text="Le texte du nouveau message"))
        content.add_widget(msg_input)
        content.add_widget(update)
        content.add_widget(cancel)
        popup = Popup(title="Editer le message",
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5},
                      content=content,
                      auto_dismiss=False)

        # définition des actions liée au button
        cancel.bind(on_press=lambda a: popup.dismiss())
        update.bind(on_press=lambda a: self.update_msg(msg, msg_input.text, collection) and popup.dismiss())
        popup.open()

    def update_msg(self, message_id, new_msg, collection):
        query = {"_id": message_id}
        new_message = {"$set": {
            "msg": new_msg
        }}
        collection.update_one(query, new_message)
        self.constant_update()

    def init_conversation_private(self, private_conversation):
        for message in private_conversation.messages:
            if message["sender"] == Main.current_user:
                msg = MessageSent(
                    text=message["timestamp"] + " - " + message["sender"] + "\n" + message["msg"])
                self.messages_box.add_widget(msg, len(self.messages_box.children))
            else:
                msg = MessageReceived(
                    text=message["timestamp"] + " - " + message["sender"] +
                         "\n" + message["msg"])
                self.messages_box.add_widget(msg, len(self.messages_box.children))

    def add_message(self, msg_obj, pos="left"):
        msg = MessageSent()  # ici
        msg.text = str(msg_obj.timestamp) + " - " + msg_obj.sender + "\n" + msg_obj.msg
        self.messages_box.add_widget(msg, len(self.messages_box.children))

    # def update_message(self, msg_obj, new_msg):
    #    msg_obj.update_msg(new_msg)
    # def update_message_on_db(self, msg_obj, new_msg):
    #     try:
    #         with MongoConnector as connector:
    #             collection = connector.db["messages"]
    #             collection.find_one_and_update({"msg": msg_obj}, {"msg": new_msg})
    #     except Exception as e:
    #         print(e)

    # def print_this(self):
    #     print("Je suis la")


class Conversation(RelativeLayout):
    def __init__(self, channel, private_conversation):
        super(Conversation, self).__init__()
        self.channel = channel
        self.private_conversation = private_conversation
        if self.channel is None:
            print(private_conversation.identifier)
            self.messages_container = ConversationContainer(channel_id=None, private_conversation=private_conversation)
        if self.private_conversation is None:
            self.messages_container = ConversationContainer(channel_id=channel.channel_id, private_conversation=None)
        self.inputs_container = InputsContainer()
        self.add_widget(self.messages_container)
        self.add_widget(self.inputs_container)

    def send_message(self):
        txt = self.inputs_container.ids.message_input.text
        timestamp = datetime.now()
        if self.private_conversation is not None:
            self.private_conversation.update_last_message(timestamp)

        if txt:
            if self.channel is None:
                msg = Message(timestamp=timestamp, msg=txt, sender=Main.current_user,
                              channel_id=None,
                              conversation_id=self.private_conversation.identifier,
                              is_edited=False)
            if self.private_conversation is None:
                msg = Message(timestamp=str(datetime.now()), msg=txt, sender=Main.current_user,
                              channel_id=self.channel.channel_id,
                              conversation_id=None,
                              is_edited=False)

            self.messages_container.add_message(msg, pos="right")
            msg.send_to_db()
            # actualise la liste des messages dans l'objet PrivateConversation
            if self.channel is None:
                self.private_conversation.update_messages_from_db()
            if txt[0] == "/":
                bot = Commands(txt)
                response_from_bot = bot.result
                msg_res = Message(datetime.now(), response_from_bot, "E-Bot")
                self.messages_container.add_message(msg_res, pos="right")

            self.inputs_container.ids.message_input.text = ""
