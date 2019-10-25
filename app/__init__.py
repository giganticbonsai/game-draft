from flask import Flask
from flask_socketio import SocketIO

from config import Config

socketio = SocketIO()
ROOMS = {}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.room import bp as room_bp
    app.register_blueprint(room_bp)

    socketio.init_app(app)
    return app
