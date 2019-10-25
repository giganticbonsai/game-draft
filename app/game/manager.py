import random
import string
from datetime import datetime

from flask import current_app


class Manager(object):

    def __init__(self, song):
        self.date_created = datetime.now()
        self.room_id = 0
        self.players = []
        self.song = song
        self.clues = {}
        self.guesses = []

        self.generate_room_id()
        self._get_clues()

    @property
    def playtime(self):
        return datetime.now() - self.date_created

    def add_player(self, name):
        self.players.append(name)

    def remove_player(self, name):
        self.players.remove(name)

    def make_guess(self, guess):
        if guess.lower() != self.song.lower():
            self.guesses.insert(0, guess)
            return 'Incorrect!'
        return self.song

    def _get_clues(self):
        self._add_clue('Clue 1', '1')
        self._add_clue('Clue 2', '2')
        self._add_clue('Clue 3', '3')
        self._add_clue('Clue 4', '4')

    def _add_clue(self, clue_name, clue):
        self.clues[clue_name] = [clue, 0]

    def open_clue(self, clue):
        self.clues[clue][1] = 1
        return self.clues[clue]

    def restart(self, song):
        self.song = song
        self.date_created = datetime.now()
        self.clues = {}
        self._get_clues()

    def jsonify(self):
        return {}

    def generate_room_id(self):
        self.room_id = ''.join(random.SystemRandom().choice(
                        string.ascii_uppercase) for _ in range(current_app.config['ROOM_ID_LENGTH']))
