import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram API credentials (from https://my.telegram.org)
    API_ID = int(os.getenv('API_ID', 0))
    API_HASH = os.getenv('API_HASH', '')
    
    # Blackbox AI API
    BLACKBOX_API_KEY = os.getenv('BLACKBOX_API_KEY', '')
    
    # Bot settings
    SESSION_NAME = os.getenv('SESSION_NAME', 'auto_chat_bot')
    ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', 0))  # Your user ID
    
    # Response settings
    RESPONSE_DELAY = 2  # seconds between responses
    MAX_MESSAGE_LENGTH = 4000
