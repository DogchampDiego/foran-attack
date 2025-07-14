from pymongo import MongoClient
import configparser
from pymongo import UpdateOne

class MongoDBWrapper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.client = None
        self.database = None
        self.collection = None
    
    def connect_db(self, collect):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        host = config.get('MongoDB', 'host')
        port = config.getint('MongoDB', 'port')
        cert = config.get('MongoDB', 'client-crt')
        ca_cert = config.get('MongoDB', 'ca-crt')
        database = config.get('MongoDB','database')
        self.database=database
        self.collection = config.get('MongoDB',collect)
        uri = f"mongodb://{host}:{port}/{database}?authMechanism=MONGODB-X509&retryWrites=true&w=majority"

        self.client = MongoClient(
            uri,
            tls=True,
            tlsCertificateKeyFile=f"{cert}",
            tlsCAFile = f"{ca_cert}",
            tlsAllowInvalidHostnames=True
        )

    def close_connection(self):
        # DB closes connection automatically but just in case.
        if self.client:
            self.client.close()
            self.client = None
    
    def insert_document(self, document):
        if self.client:
            db = self.client[self.database]
            coll = db[self.collection]
            result = coll.insert_one(document)
            return result.inserted_id
        else:
            raise ValueError("Connection to MongoDB not established.")

    def insert_document_from_file(self, document):
        if self.client:
            db = self.client[self.database]
            coll = db[self.collection]
            result = coll.insert_one(document)
            return result.inserted_id
        else:
            raise ValueError("Connection to MongoDB not established.")

    def find_documents(self, query=None):
        db = self.client[self.database]
        col = db[self.collection]
        if query:
            return col.find(query)
        else:
            return col.find()


    def update_document(self, document_id, key_to_update, new_value):
        if self.client:
            db = self.client[self.database]
            coll = db[self.collection]

            # Construct an update query to update the document by its _id
            update_query = {"_id": document_id}

            # Construct an update operation to set a new value for the specified key
            update_operation = {
                "$set": {key_to_update: new_value}
            }

            # Create an UpdateOne object
            update_request = UpdateOne(update_query, update_operation)

            try:
                # Execute the update operation
                result = coll.bulk_write([update_request])
                return result.modified_count
            except Exception as e:
                print(f"Error updating document: {str(e)}")
                return 0  # Return 0 to indicate that no documents were updated
        else:
            raise ValueError("Connection to MongoDB not established.")
