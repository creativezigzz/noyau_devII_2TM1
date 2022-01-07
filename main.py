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
import uuid

from dotenv import load_dotenv
from kivy.app import App
from kivy.lang import Builder

import src.config.config as config
from src.models.screens_manager import ScreensManager
from src.utils import db_delete_document, db_verify

load_dotenv()

Builder.load_file("{0}/common.kv".format(config.VIEWS_DIR))


class Main(App):
    title = 'EpheCom'
    current_user = "Vincent"
    current_user_logged = ["Vincent", "Alice", "Mady"]

    def build(self):
        from src.views.landing import LandingScreen

        sm = ScreensManager()
        landing_screen = LandingScreen()
        sm.add_widget(landing_screen)
        sm.current = "landing"
        # Juste pour simplifier les tests sur la DB
        # db_delete_document.delete_collection("teams")
        # db_delete_document.delete_collection("channels")
        # db_delete_document.delete_collection("messages")
        # db_delete_document.delete_collection("private_messages")
        # db_verify.verification_collection("teams")
        # db_verify.verification_collection("channels")
        # db_verify.verification_collection("messages")
        # db_verify.verification_collection("private_messages")
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
