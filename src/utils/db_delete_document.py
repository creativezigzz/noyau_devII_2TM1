from src.models.mongo_connector import MongoConnector


def delete_collection(name_collection):
    # suppression des channels en DB
    # delete_channel = connector.db["channels"].delete_many({})
    # print(delete_channel.deleted_count, " channels deleted.")

    # suppression des messages en DB
    # delete_messages = connector.db["messages"].delete_many({})
    # print(delete_messages.deleted_count, " messages deleted.")
    try:
        with MongoConnector() as connector:
            delete = connector.db[name_collection].delete_many({})
            print(delete().deleted_count, " documents deleted.")

    except Exception as e:
        print(e)
