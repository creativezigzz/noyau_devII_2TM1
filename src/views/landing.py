#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente l'interface de lancement de l'application.
    Cette interface contient 3 zones distinctes :
        - Le header de notre application
        - La liste de nos différents channels/groupes
        - La zone de contenu de nos channels après sélection d'un channel.
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from src.config import config
from src.models.channel import Channel
from src.models.private_messages import PrivateConversation
from src.models.screens_manager import ScreensManager
from src.models.team import Team
from src.views.conversation import Conversation
from src.views.private_conversation import PrivateConversationContainer
from src.views.teams_container import TeamsContainer
from src.views.channels import ChannelsContainer, ParticipantContainer

Builder.load_file("{0}/header.kv".format(config.VIEWS_DIR))
Builder.load_file("{0}/landing.kv".format(config.VIEWS_DIR))


class LandingScreen(Screen):
    def __init__(self):
        super(LandingScreen, self).__init__()
        self.name = "landing"
        self.sm = ScreensManager()
        self.conv_box = self.ids.conversation_box
        self.team_box = self.ids.channels_box
        self.rooms_box = self.ids.rooms_box
        self.participant_box = self.ids.participants_box
        self.teams_container = None

    def redirect_to_href(self, href: str):
        """
            [Base]
            Gestion des évènements de redirection du Screen.
            :param href : Le nom du Screen vers lequel naviguer.
        """
        self.sm.redirect(href)

    def display_channels(self, channels_current_team: list, team: Team):
        """
            [Base]
            Permet la mise à jour de la liste des "Channel" après un clic sur le nom d'une "Team".
            :param channels_current_team : Liste des 'Channel' de la "Team" concernée.
            :param team : l'objet Team concernant la team actuellement utilisée
        """
        self.conv_box.clear_widgets()
        self.participant_box.clear_widgets()
        self.rooms_box.clear_widgets()
        self.rooms_box.add_widget(ChannelsContainer(channels_current_team, team))

    def display_conversation(self, channel: Channel, private_conversation: PrivateConversation):
        """
            [Base]
            Permet la mise à jour de la conversation active après un clic sur le nom d'un "Channel".
            :param channel : l'objet Channel dont cherche à afficher les messages
            :param private_conversation : l'objet PrivateConversation dont cherche à afficher les messages
        """
        self.conv_box.clear_widgets()
        conversation = Conversation(channel, private_conversation)
        self.conv_box.add_widget(conversation)

    def display_participant_channel(self, member_list: list, channel: list, team: list):
        """
            Permet la mise à jour des participants du channel après un clic sur le nom d'un "Channel".
            :param member_list : La liste des membres du channel
            :param channel : La liste des channels
            :param team : La team
        """
        self.participant_box.clear_widgets()
        member = ParticipantContainer(member_list, channel, team, display_channels_member=True,
                                      conversation=None,
                                      display_team_member=False)
        self.participant_box.add_widget(member)

    def set_teams_list(self):
        """
            [Base]
            Initialise la liste des "Team" dont l'utilisateur fait partie.
        """
        self.teams_container = TeamsContainer()
        self.team_box.add_widget(self.teams_container)

    # peut-être a supprimé
    def display_participant_team(self, team: Team):
        """
            Permet la mise à jour des participants de la team après un clic sur le nom d'une team.
            :param team : La team
        """
        self.participant_box.clear_widgets()
        member = ParticipantContainer(member_list=team.participants, channel=None, team=team,
                                      conversation=None,
                                      display_channels_member=False, display_team_member=True)
        self.participant_box.add_widget(member)

    def display_private_conversation(self):
        self.conv_box.clear_widgets()
        self.participant_box.clear_widgets()
        self.rooms_box.clear_widgets()
        self.rooms_box.add_widget(PrivateConversationContainer())
        print("afficher les conversation privées")

    def display_participant_conversation(self, conversation):
        self.participant_box.clear_widgets()
        member = ParticipantContainer(member_list=conversation.members, channel=None, team=None,
                                      conversation=conversation,
                                      display_channels_member=False, display_team_member=True)
        self.participant_box.add_widget(member)
