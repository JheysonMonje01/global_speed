import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MIKROTIK_HOST = os.getenv("MIKROTIK_HOST")
    MIKROTIK_USER = os.getenv("MIKROTIK_USERNAME")
    MIKROTIK_PASS = os.getenv("MIKROTIK_PASSWORD")
