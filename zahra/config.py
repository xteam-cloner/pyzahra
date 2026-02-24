import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    
    DB_NAME = "zahraDB"
    COL_NAME = "sessions"
    
    BASE_DIR = os.getcwd()
    RES_PATH = os.path.join(BASE_DIR, "resources")
  
