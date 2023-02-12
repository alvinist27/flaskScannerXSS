import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
STATIC_PATH = os.path.join(BASE_DIR, 'static')

DB_STRING_LENGTH = 255
SECRET_KEY_LENGTH = 32
