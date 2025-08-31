import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci_rahasia_simdes'
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'Qwerty77'
    DB_NAME = 'simdes_db'
