import os

# --- FIX: Define BASE_DIR before using it ---
# This creates an absolute path to the directory containing this config file (your project root).
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --- Application Settings ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key-that-you-should-change')
DEBUG = True

# --- Database Settings ---
# Use BASE_DIR to create a reliable path to your database file.
DB_PATH = os.path.join(BASE_DIR, 'instance', 'career_advisor.db')

# --- Mock User Settings ---
# These are used by auth.py and models.py to enable local testing without login.
MOCK_USER_MODE = True
MOCK_USER_EMAIL = 'mock@student.com'
MOCK_USER_PASSWORD = 'mockpassword'
MOCK_USER_ID = None      # This will be set at runtime by the application
MOCK_USER_TOKEN = None  # This will be set at runtime by the application
TOKEN_TTL_DAYS = 30

