import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://posterr_admin:123456@localhost/posterr')
    SQLALCHEMY_TRACK_MODIFICATIONS = False