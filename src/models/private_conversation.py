from bson import timestamp

from src.models.mongo_connector import MongoConnector


class PrivateConversation:
    def __init__(self, id: str, name: str, members: list, last_message):
        self._id = id
        self.name = name
        self.members = members
        self.last_message = last_message
        self.messages = []
        self.get_messages_from_db()
        try:
            with MongoConnector() as connector:
                self.__collection = connector.db["private_messages"]
        except Exception as error:
            print(error)

    @property
    def identifier(self):
        return self._id

    def add_member(self, new_member):
        # ajout dans l'objet
        self.members.append(new_member)
        # ajout dans la DB
        query = {"_id": self._id}
        new_member = {"$set": {
            "members": self.members
        }}
        self.__collection.update_one(filter=query, update=new_member)

    def update_last_message(self, new_timestamp):
        self.last_message = new_timestamp
        query = {"_id": self._id}
        new_last_message = {"$set": {
            "last_message": self.last_message
        }}
        self.__collection.update_one(filter=query, update=new_last_message)

    def get_messages_from_db(self):
        try:
            with MongoConnector() as connector:
                collection_messages = connector.db["messages"]
                for message in collection_messages.find():
                    if message["channel_id"] is None:
                        if message["conversation_id"] == str(self._id):
                            self.messages.append(message)
        except Exception as error:
            print(error)

    def update_messages_from_db(self):
        self.messages = []
        self.get_messages_from_db()
