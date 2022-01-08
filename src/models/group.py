#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import traceback
import uuid

"""
    Ce fichier contient une classe représentant un groupe.
    ----- CODE DE LA CLASSE A IMPLEMENTER -----
"""


class Group:
    def __init__(self, name):
        self.gid = uuid.uuid4()
        self.name = name

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb)
        return True
