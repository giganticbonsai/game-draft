import os

from flask.cli import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'to-be-set'
    SEND_FILE_MAX_AGE_DEFAULT = 0
    ROOM_ID_LENGTH = 5
    ROOM_TIME_LIMIT = 300
    ROOM_UPDATE_INTERVAL = 1
