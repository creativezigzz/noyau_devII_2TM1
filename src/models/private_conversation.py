import uuid

from src.models.mongo_connector import MongoConnector


class PrivateConversation:
    def __init__(self, id, name: str, members: list, last_message=None):
        """init a new private conversation"""
        """
        PRE : name is a str, members is a list of str
        POST : a new private conversation is created
        """
        if id is None:
            self._id = uuid.uuid4()
        else:
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

    def send_conversation_on_db(self):
        """send the conversation to the db"""
        query = {'_id': self._id,
                 'name': self.name,
                 'members': self.members,
                 'last_message': self.last_message
                 }
        self.__collection.insert_one(query)

    def add_member(self, new_member):
        """add 'new_member' to the members list"""
        """
        PRE : new_member is a string
        POST : new_member is added to the list 'members'
        """
        # ajout dans l'objet
        self.members.append(new_member)
        # ajout dans la DB
        query = {"_id": self._id}
        new_member = {"$set": {
            "members": self.members
        }}
        self.__collection.update_one(filter=query, update=new_member)

    def remove_member(self):
        pass

    def update_last_message(self, new_timestamp):
        """update the last message of the conversation"""
        """
        PRE : new_timestamp is a datetime object
        POST : the last message is changed
        """
        self.last_message = new_timestamp
        query = {"_id": self._id}
        new_last_message = {"$set": {
            "last_message": self.last_message
        }}
        self.__collection.update_one(filter=query, update=new_last_message)

    def get_messages_from_db(self):
        """init the messages from the db"""
        self.messages = []
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
        """init the messages from the db"""
        self.get_messages_from_db()
