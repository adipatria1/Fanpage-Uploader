import os
from dotenv import load_dotenv

load_dotenv()

# Facebook API Configuration
USER_ACCESS_TOKEN = os.getenv('FB_USER_ACCESS_TOKEN', 'YOUR_TOKEN')
API_VERSION = 'v21.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

# Upload Configuration
TEMP_UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(TEMP_UPLOAD_FOLDER):
    os.makedirs(TEMP_UPLOAD_FOLDER)