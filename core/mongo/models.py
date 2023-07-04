import pymongo
import settings

host = settings.MONGO_CONFIG.host
port = settings.MONGO_CONFIG.port
db_name = settings.MONGO_CONFIG.db_name
collection_name = settings.MONGO_CONFIG.collection_name

client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
db = client[db_name]
collection = db[collection_name]
