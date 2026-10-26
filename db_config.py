"""
MySQL connection settings for the IRCTC Railway Ticketing System.
Credentials are loaded from a .env file (see .env.example).
"""

import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "railway_db"),
}
