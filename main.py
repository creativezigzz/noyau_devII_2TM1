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
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput

import src.config.config as config
from src.models.screens_manager import ScreensManager
from src.models.user import User
from src.utils import db_delete_document, db_verify

load_dotenv()

Builder.load_file("{0}/common.kv".format(config.VIEWS_DIR))


def set_user(pseudo):
    new_user: User
    if pseudo != "":
        new_user = User(uid=uuid.uuid4(), pseudo=pseudo, current_user=True)
        return new_user
    else:
        print("erreur")
        login()


def login():
    content = RelativeLayout()
    current_user_input = TextInput(text='', font_size=14, size_hint_y=None, height=50,
                                   pos_hint={'center_x': .5, 'center_y': .3})
    login_button = Button(text="Login", size_hint=(None, None), size=(150, 40),
                          pos_hint={'center_x': .4, 'center_y': .1})
    # ajout des button, de l'input et du label a la popup
    content.add_widget(Label(text="Votre pseudo :"))
    content.add_widget(current_user_input)
    content.add_widget(login_button)
    popup = Popup(title="identifiez vous",
                  size_hint=(.5, .5),
                  pos_hint={'center_x': .5, 'center_y': .5},
                  content=content,
                  auto_dismiss=False)
    # définition des actions liée au button
    login_button.bind(on_press=lambda a: set_user(current_user_input.text) and popup.dismiss())
    popup.open()


class Main(App):
    title = 'EpheCom'
    current_user = "Vincent"

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
        db_verify.verification_collection("teams")
        db_verify.verification_collection("channels")
        db_verify.verification_collection("messages")
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
