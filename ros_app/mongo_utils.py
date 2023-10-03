import pymongo

# MongoDB connection details from Django settings
from django.conf import settings
mongo_settings = settings.DATABASES['default']
# Function to get a MongoDB client
def get_mongo_client():
    
    client = pymongo.MongoClient(
        host=mongo_settings['HOST'],
        port=mongo_settings['PORT'],
        username=mongo_settings['USER'],
        password=mongo_settings['PASSWORD'],
        ssl=mongo_settings['OPTIONS']['ssl']
    )
    return client

# Function to get a MongoDB database
def get_mongo_database(db_name=None):
    
    client = get_mongo_client()
    if db_name:
        return client[db_name]
    else:
        return client[mongo_settings['NAME']]
