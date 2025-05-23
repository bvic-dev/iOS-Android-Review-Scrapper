import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        # ---- iOS App Store Connect ----
        self.KEY_ID = os.getenv('KEY_ID', 'DEFAULT_KEY_ID')
        self.ISSUER_ID = os.getenv('ISSUER_ID', 'DEFAULT_ISSUER_ID')
        self.PRIVATE_KEY_FILE = os.getenv('PRIVATE_KEY_FILE', 'PRIVATE_KEY_FILE')
        self.APPLE_APP_ID = os.getenv('APPLE_APP_ID', 'APPLE_APP_ID')
        try:
            # Load the iOS private key from file
            with open(self.PRIVATE_KEY_FILE, 'r') as f:
                self.PRIVATE_KEY = f.read()
        except FileNotFoundError:
            print(f"⚠️ Could not find PRIVATE_KEY_FILE: {self.PRIVATE_KEY_FILE}")
            self.PRIVATE_KEY = ""

        # ---- Android Google Play ----
        self.JSON_KEY_FILE = os.getenv('JSON_KEY_FILE', 'JSON_KEY_FILE')
        self.REPO_PACKAGE_NAME = os.getenv('REPO_PACKAGE_NAME', 'DEFAULT_APP_PACKAGE_ID')
        
        # ---- General settings ----
        self.OUTPUT_FILE = None
        self.TIMEDELTA_HOURS = 72
        self.REVIEWS_FETCH_QUANTITY = 50
        self.DATETIME_FORMAT = "%d/%m/%y %H:%M:%S"
        
        # ---- Discord ----
        self.DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', 'DEFAULT_DISCORD_WEBHOOK_URL')

config = Config()
