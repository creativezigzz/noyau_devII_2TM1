import traceback

from pymongo import MongoClient

from src.config import config


class MongoConnector:
    """
        Cette classe permet de créer une connexion vers la base de données.

        Veuillez modifier la variable 'certificat_path' avec le chemin vers l'endroit ou se trouve votre certificat.

        Exemple d'utilisation dans votre code :

        try:
            with MongoConnector() as connector:
                collection = connector.db["users"]
                res = collection.find_one()
                print(res)
        except Exception as e:
            print(e)
    """

    def __init__(self):
        certificat_path = config.ROOT_DIR + "/2TM1-G3.pem"
        uri = "mongodb+srv://cluster0.5i6qo.gcp.mongodb.net/ephecom?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE"
        client = MongoClient(uri,
                             tls=True,
                             tlsCertificateKeyFile=certificat_path)
        self.db = client['ephecom']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb)
        self.db.close()
        return True

