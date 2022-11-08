import os


class Config:
    SECRET_KEY = '5af89320adcea26843513782275cdc7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER') or 'temmyghold00@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
