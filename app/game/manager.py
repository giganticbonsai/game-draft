import random
import string
from datetime import datetime, timedelta

from flask import current_app


class Manager(object):

    def __init__(self, song, duration=5):
        self.room_id = 0
        self.players = []

        self.generate_room_id()
        self._start_game(song, duration)

    def _start_game(self, song, duration):
        self.date_end = datetime.utcnow() + timedelta(minutes=duration)
        self.song = song
        self.clues = {}
        self.hidden_clues = []
        self.guesses = []
        self._load_clues()

    @property
    def playtime(self):
        if self.date_end <= datetime.utcnow():
            return
        td = self.date_end - datetime.utcnow()
        time_since = divmod(td.days*86400 + td.seconds, 60)
        return '{0} minutes, {1:02d} seconds'.format(time_since[0], time_since[1])

    @property
    def latest_guess(self):
        return self.guesses[0:10]

    def add_player(self, name):
        self.players.append(name)

    def remove_player(self, name):
        self.players.remove(name)

    def is_song(self, guess):
        if guess.lower() != self.song.lower():
            self.guesses.insert(0, guess)
            return False
        return True

    def _load_clues(self):
        self._add_clue('Clue_1', '1')
        self._add_clue('Clue_2', '2')
        self._add_clue('Clue_3', '3')
        self._add_clue('Clue_4', '4')
        self.hidden_clues = self.clues.keys()

    def _add_clue(self, clue_name, clue):
        self.clues[clue_name] = [clue, 'HIDDEN']

    def open_clue(self, clue):
        return self.clues[clue][0]

    def next_clue(self):
        if self.hidden_clues:
            reveal = self.hidden_clues.pop()
            return reveal

    def jsonify(self):
        return {
            'playtime': self.playtime}

    def generate_room_id(self):
        self.room_id = ''.join(random.SystemRandom().choice(
                        string.ascii_uppercase) for _ in range(current_app.config['ROOM_ID_LENGTH']))

    def end_game(self):
        while self.hidden_clues:
            self.open_clue(self.next_clue())

