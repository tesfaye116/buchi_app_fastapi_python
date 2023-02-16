from config.config import Settings
import motor.motor_asyncio


settings = Settings()

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
except Exception as e:
    print("!Oops, something went wrong with the database connection")

database = client[settings.MONGO_INITDB_DATABASE]


def get_collection(collection_name: str):
    return database.get_collection(collection_name)
