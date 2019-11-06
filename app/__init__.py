from flask import Flask
from flask_socketio import SocketIO

from app.spotify.auth import SpotifyCredentials
from app.spotify.spotify import Spotify
from config import Config

socketio = SocketIO()
ROOMS = {}
spotify_auth = SpotifyCredentials()
spotify = Spotify(spotify_auth)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.room import bp as room_bp
    app.register_blueprint(room_bp)

    socketio.init_app(app)
    return app
