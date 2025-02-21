#src/__init__.py
import os

# Cargar variables de entorno de .env
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    VERIFY_TOKEN_WEBHOOK = os.getenv('VERIFY_TOKEN_WEBHOOK')
    WHATSAPP_VERSION = os.getenv('WHATSAPP_VERSION')
    ASSIST_HUMAN_TAG = os.getenv('ASSIST_HUMAN_TAG')
    
print(f"SQLALCHEMY_DATABASE_URI: {Config.SQLALCHEMY_DATABASE_URI}")  # Para verificar la carga

# Resto del código de create_app() ...
