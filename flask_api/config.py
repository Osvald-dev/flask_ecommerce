from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    # SERVER_NAME = 'localhost'
    # SESSION_COOKIE_SECURE = False 