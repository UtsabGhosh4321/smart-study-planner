from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

# Get MongoDB URL from .env
MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Create MongoDB client
client = AsyncIOMotorClient(
    MONGO_URL,
    tlsCAFile=certifi.where()
)

# Select database
db = client[DATABASE_NAME]