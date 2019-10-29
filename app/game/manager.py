import random
import string
from datetime import datetime, timedelta

from flask import current_app


class Manager(object):

    def __init__(self, song, duration=5):
        self.date_end = datetime.utcnow() + timedelta(minutes=duration)
        self.room_id = 0
        self.players = []
        self.song = song
        self.clues = {}
        self.guesses = []
        self.time_limit = 300  # seconds

        self.generate_room_id()
        self._load_clues()

    @property
    def playtime(self):
        if self.date_end <= datetime.utcnow():
            return 'TIMES UP!'
        td = self.date_end - datetime.utcnow()
        time_since = divmod(td.days*86400 + td.seconds, 60)
        return '{0} minutes, {1:02d} seconds'.format(time_since[0], time_since[1])

    def add_player(self, name):
        self.players.append(name)

    def remove_player(self, name):
        self.players.remove(name)

    def make_guess(self, guess):
        if guess.lower() != self.song.lower():
            self.guesses.insert(0, guess)
            return 'Incorrect!'
        return self.song

    def _load_clues(self):
        self._add_clue('Clue_1', '1')
        self._add_clue('Clue_2', '2')
        self._add_clue('Clue_3', '3')
        self._add_clue('Clue_4', '4')

    def _add_clue(self, clue_name, clue):
        self.clues[clue_name] = [clue, 0]

    def open_clue(self, clue):
        self.clues[clue][1] = 1
        return self.clues[clue][0]

    def restart(self, song):
        pass

    def jsonify(self):
        return {
            'time_limit': self.time_limit,
            'playtime': self.playtime}

    def generate_room_id(self):
        self.room_id = ''.join(random.SystemRandom().choice(
                        string.ascii_uppercase) for _ in range(current_app.config['ROOM_ID_LENGTH']))
