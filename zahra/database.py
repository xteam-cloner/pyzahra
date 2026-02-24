from motor.motor_asyncio import AsyncIOMotorClient
from .config import Config

db_client = AsyncIOMotorClient(Config.MONGO_URL)
db = db_client[Config.DB_NAME]
collection = db[Config.COL_NAME]
