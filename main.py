#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Projet EpheCom
    ===================================

    Ce logiciel a été développé dans le cadre scolaire.
    EpheCom est un logiciel de communications - vocale et écrite - en temps réel.
    Il a pour but d'améliorer la communication au sein de l'établissement scolaire.

    Version de Python : 3.9
    Système d'exploitation : Windows, OSX, Linux
    Type : Application de bureau
    Language utilisé pour coder : Anglais
    Language utilisé pour documenter : Français
    Documentation Framework : https://kivy.org/doc/stable/api-kivy.html
    Source unique des icons : https://remixicon.com/

    Convention de nommage :
        https://www.python.org/dev/peps/pep-0008/

"""
from uuid import UUID

from dotenv import load_dotenv
from kivy.app import App
from kivy.lang import Builder

import src.config.config as config
from src.models.mongo_connector import MongoConnector
from src.models.screens_manager import ScreensManager

load_dotenv()

Builder.load_file("{0}/common.kv".format(config.VIEWS_DIR))


def verification_collection():
    try:
        with MongoConnector() as connector:
            print(connector.db.list_collection_names())
            # print(connector.db["messages"].find_one())
            # suppression des teams en DB
            # delete_team = connector.db["teams"].delete_many({})
            # print(delete_team.deleted_count, " teams deleted.")
            # suppression des channels en DB
            # delete_channel = connector.db["channels"].delete_many({})
            # print(delete_channel.deleted_count, " channels deleted.")
            # delete_messages = connector.db["messages"].delete_many({})
            # print(delete_messages.deleted_count, " messages deleted.")
            if connector.db["teams"].find_one() is None:
                print("team est vide")
                set_collection_team()
            if connector.db["channels"].find_one() is None:
                print("channels est vide")
                set_collection_channel()
            if connector.db["messages"].find_one() is None:
                print("messages est vide")
                set_collection_message()
            else:
                print("ok data correctes")
            for x in connector.db["teams"].find():
                print(x)
            for x in connector.db["channels"].find():
                print(x)
            for x in connector.db["messages"].find():
                print(x)

    except Exception as e:
        print(e)


def set_collection_message():
    data = [{'_id': UUID('7d7c46d1-45a8-4efa-afdd-78a87a2c9dc3'),
             'timestamp': '2021-12-22 18:01:00.287792',
             'msg': 'test',
             'sender': 'Moi',
             'is_edited': False,
             'channel_id': 'b816ef54-7a5c-448a-972c-78267ae371c6'},

            {'_id': UUID('cae144f6-2c9c-4096-a5c1-572c1807e065'),
             'timestamp': '2021-12-22 18:01:11.343219',
             'msg': 'pour que ça fonctionne',
             'sender': 'Moi',
             'is_edited': False,
             'channel_id': 'b816ef54-7a5c-448a-972c-78267ae371c6'},

            {'_id': UUID('8a8d50a0-7a69-4870-970d-810ebeed20ea'),
             'timestamp': '2021-12-22 18:05:21.004276',
             'msg': 'Hello bonjour',
             'sender': 'Moi',
             'is_edited': False,
             'channel_id': 'b816ef54-7a5c-448a-972c-78267ae371c6'},

            {'_id': UUID('4a2b4ff1-c3df-43d0-8d08-c535d15624b2'),
             'timestamp': '2021-12-22 18:05:29.721733',
             'msg': "Hello c'est moi",
             'sender': 'Moi',
             'is_edited': False,
             'channel_id': "a11b4ee7-8743-4607-b838-acc1298a5f7a"},

            {'_id': UUID('f3525263-02d9-4b75-8b23-5dfe619e95b8'),
             'timestamp': '2021-12-23 10:35:59.314162',
             'msg': 'test 10h35',
             'sender': 'Moi',
             'is_edited': False,
             'channel_id': "a11b4ee7-8743-4607-b838-acc1298a5f7a"}]
    try:
        with MongoConnector() as connector:
            db = connector.db
            collection_messages = db["messages"]
            collection_messages.insert_many(data)

    except Exception as e:
        print(e)


def set_collection_team():
    # données qui sont en Db utilisé lors de la recréation de la collection

    data_teams1 = [{
        "name": "Pis",
        "icon_path": "",
        "participants": [
            "SerialMatcher",
            "Bilou",
            "Babar",
            "Jacques",
            "Vincent",
            "Mady",
            "Oli",
            "Alice",
            "Lucas",
        ],
        "channel_id": ["a11b4ee7-8743-4607-b838-acc1298a5f7a",
                       "a11b4ee7-8743-4607-b838-acc1298a5fer",
                       "a11b4ee7-8743-4607-b838-acc1298arrr",
                       "a11b4ee7-8743-4607-b838-acc1298a5f7b"
                       ]
    },
        {
            "name": "Pan",
            "icon_path": "",
            "participants": [
                "SerialMatcher",
                "Bilou",
                "Babar",
                "Jacques",
                "Vincent",
                "Mady",
                "Oli",
                "Alice",
                "Toulouse",
                "Adrien",
                "Bastien",
            ],
            "channel_id": [
                "b816ef54-7a5c-448a-972c-78267ae371c6",
                "b816ef54-7a5c-448a-972c-78267ae371az",
                "b816ef54-7a5c-448a-972c-78267ae371tb",
            ]
        }]
    try:
        with MongoConnector() as connector:
            db = connector.db
            collection_team = db["teams"]
            collection_team.insert_many(data_teams1)
            # collection_team.insert_many(data_teams2)
    except Exception as e:
        print(e)


def set_collection_channel():
    data_channel = [
        {"channel_id": "a11b4ee7-8743-4607-b838-acc1298a5f7a",
         "name": "pis",
         "admin": "Bilou",
         "group": "group_test1",
         "membres": ["SerialMatcher",
                     "Jacques",
                     "Alice"]},
        {"channel_id": "a11b4ee7-8743-4607-b838-acc1298a5fer",
         "name": "channel_de_test1",
         "admin": "Bilou",
         "group": "group_test1",
         "membres": ["SerialMatcher",
                     "Jacques",
                     "Vincent",
                     "Alice"]},
        {"channel_id": "a11b4ee7-8743-4607-b838-acc1298arrr",
         "name": "channel_de_test2",
         "admin": "Bilou",
         "group": "group_test2",
         "membres": ["SerialMatcher",
                     "Jacques"]},
        {"channel_id": "a11b4ee7-8743-4607-b838-acc1298a5f7b",
         "name": "channel_de_test3",
         "admin": "Bilou",
         "group": "group_test2",
         "membres": ["SerialMatcher",
                     "Jacques",
                     "SerialMatcher"]},
        {"channel_id": "b816ef54-7a5c-448a-972c-78267ae371c6",
         "name": "channel_de_test1",
         "admin": "Bilou",
         "group": "group_test1",
         "membres": ["SerialMatcher",
                     "Jacques"]},
        {"channel_id": "b816ef54-7a5c-448a-972c-78267ae371az",
         "name": "channel_de_test2",
         "admin": "Bilou",
         "group": "group_test1",
         "membres": ["SerialMatcher",
                     "Jacques"]},
        {"channel_id": "b816ef54-7a5c-448a-972c-78267ae371tb",
         "name": "channel_de_test3",
         "admin": "Bilou",
         "group": "group_test2",
         "membres": ["SerialMatcher",
                     "Babar"]}
    ]
    try:
        with MongoConnector() as connector:
            db = connector.db
            collection_channel = db["channels"]
            collection_channel.insert_many(data_channel)
    except Exception as e:
        print(e)


class Main(App):
    title = 'EpheCom'

    def build(self):
        from src.views.landing import LandingScreen

        sm = ScreensManager()
        landing_screen = LandingScreen()
        sm.add_widget(landing_screen)
        sm.current = "landing"
        verification_collection()
        landing_screen.set_teams_list()
        return sm


class Personne:
    def __init__(self, nom):
        self.nom = nom


class Etudiant(Personne):
    def __init__(self, nom):
        super(Etudiant, self).__init__(nom)


if __name__ == '__main__':
    print("Bienvenue sur notre projet commun !")
    Main().run()

ancienne_data1 = [{
    "_id": "0000000",
    "data": {
        "name": "Pis",
        "icon_path": "",
        "participants": [
            {"pseudo": "SerialMatcher"},
            {"pseudo": "Bilou"},
            {"pseudo": "Babar"},
            {"pseudo": "Jacques"},
        ],
        "channels": [
            {"id": "a11b4ee7-8743-4607-b838-acc1298a5f7a",
             "name": "pis",
             "admin": "Bilou",
             "group": "group_test1",
             "membres": [{"pseudo": "SerialMatcher"},
                         {"pseudo": "Jacques"}]},
            {"id": "a11b4ee7-8743-4607-b838-acc1298a5fer",
             "name": "channel_de_test1",
             "admin": "Bilou",
             "group": "group_test1",
             "membres": [{"pseudo": "SerialMatcher"},
                         {"pseudo": "Jacques"}]},
            {"id": "a11b4ee7-8743-4607-b838-acc1298arrr",
             "name": "channel_de_test2",
             "admin": "Bilou",
             "group": "group_test2",
             "membres": [{"pseudo": "SerialMatcher"},
                         {"pseudo": "Jacques"}]},
            {"id": "a11b4ee7-8743-4607-b838-acc1298a5f7b",
             "name": "channel_de_test3",
             "admin": "Bilou",
             "group": "group_test2",
             "membres": [{"pseudo": "SerialMatcher"},
                         {"pseudo": "Jacques"},
                         {"pseudo": "SerialMatcher"}]}
        ]
    }
}]
ancienne_data2 = [{
    "_id": "0000001",
    "data": {
        "name": "Pan",
        "icon_path": "",
        "participants": [
            {"pseudo": "SerialMatcher"},
            {"pseudo": "Bilou"},
            {"pseudo": "Babar"},
            {"pseudo": "Jacques"},
        ],
        "channels": [
            {"id": "b816ef54-7a5c-448a-972c-78267ae371c6",
             "name": "channel_de_test1",
             "admin": "Bilou",
             "group": "group_test1",
             "membres": [{"pseudo": "SerialMatcher"},
                         {"pseudo": "Jacques"}]},
            {"id": "b816ef54-7a5c-448a-972c-78267ae371az",
             "name": "channel_de_test2",
             "admin": "Bilou",
             "group": "group_test1",
             "membres": [{"pseudo": "SerialMatcher"},
                         {"pseudo": "Jacques"}]},
            {"id": "b816ef54-7a5c-448a-972c-78267ae371tb",
             "name": "channel_de_test3",
             "admin": "Bilou",
             "group": "group_test2",
             "membres": [{"pseudo": "SerialMatcher"},
                         {"pseudo": "Babar"}]}
        ]
    }}]
