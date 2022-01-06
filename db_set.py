from uuid import UUID

from src.models.mongo_connector import MongoConnector

data_messages = [
    {'_id': UUID('7d7c46d1-45a8-4efa-afdd-78a87a2c9dc3'),
     'timestamp': '2021-12-22 18:01:00.287792',
     'msg': 'test',
     'sender': 'Jacques',
     'is_edited': False,
     'channel_id': 'b816ef54-7a5c-448a-972c-78267ae371c6'},

    {'_id': UUID('cae144f6-2c9c-4096-a5c1-572c1807e065'),
     'timestamp': '2021-12-22 18:01:11.343219',
     'msg': 'pour que ça fonctionne',
     'sender': 'Vincent',
     'is_edited': False,
     'channel_id': 'b816ef54-7a5c-448a-972c-78267ae371c6'},

    {'_id': UUID('8a8d50a0-7a69-4870-970d-810ebeed20ea'),
     'timestamp': '2021-12-22 18:05:21.004276',
     'msg': 'Hello bonjour',
     'sender': 'Babar',
     'is_edited': False,
     'channel_id': 'b816ef54-7a5c-448a-972c-78267ae371c6'},

    {'_id': UUID('4a2b4ff1-c3df-43d0-8d08-c535d15624b2'),
     'timestamp': '2021-12-22 18:05:29.721733',
     'msg': "Hello c'est moi",
     'sender': 'Vincent',
     'is_edited': False,
     'channel_id': "a11b4ee7-8743-4607-b838-acc1298a5f7a"},

    {'_id': UUID('f3525263-02d9-4b75-8b23-5dfe619e95b8'),
     'timestamp': '2021-12-23 10:35:59.314162',
     'msg': 'test 10h35',
     'sender': 'Bilou',
     'is_edited': False,
     'channel_id': "a11b4ee7-8743-4607-b838-acc1298a5f7a"}]

data_teams = [{
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


def set_collection_message():
    try:
        with MongoConnector() as connector:
            db = connector.db
            collection_messages = db["messages"]
            collection_messages.insert_many(data_messages)

    except Exception as e:
        print(e)


def set_collection_team():
    try:
        with MongoConnector() as connector:
            db = connector.db
            collection_team = db["teams"]
            collection_team.insert_many(data_teams)
            # collection_team.insert_many(data_teams2)
    except Exception as e:
        print(e)


def set_collection_channel():
    try:
        with MongoConnector() as connector:
            db = connector.db
            collection_channel = db["channels"]
            collection_channel.insert_many(data_channel)
    except Exception as e:
        print(e)
