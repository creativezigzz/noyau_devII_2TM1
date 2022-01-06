import db_set
from src.models.mongo_connector import MongoConnector


def verification_collection(collection_name: str):
    """
    Vérifie que les collections teams, channels et messages
    Si une collection est vide
    """
    try:
        with MongoConnector() as connector:
            print(connector.db.list_collection_names())
            # print(connector.db["messages"].find_one())

            # création des collections si elles sont vides
            if connector.db[collection_name].find_one() is None:
                print(collection_name + " est vide")
                if collection_name == "teams":
                    db_set.set_collection_team()
                if collection_name == "messages":
                    db_set.set_collection_message()
                if collection_name == "channels":
                    db_set.set_collection_channel()
            else:
                print("ok collection " + collection_name + " is not empty")

            # affichage en console des différents documents de la collection
            for x in connector.db[collection_name].find():
                print(x)

    except Exception as e:
        print(e)

