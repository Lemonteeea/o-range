import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'Just-see-if-you-can-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:222222222@localhost:3306/orange'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

