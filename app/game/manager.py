from __future__ import division
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
        self.clue_index = {}
        self.hidden_clues = []
        self.guesses = []
        self._load_clues()
        self.open_clue_interval = duration/(len(self.hidden_clues)+1)

    @property
    def playtime(self):
        if self.date_end <= datetime.utcnow():
            return
        td = self.date_end - datetime.utcnow()
        time_since = divmod(td.days*86400 + td.seconds, 60)
        return [td, '{0} minutes, {1:02d} seconds'.format(time_since[0], time_since[1])]

    @property
    def latest_guess(self):
        return self.guesses[0:10]

    @property
    def clues(self):
        clues = {}
        for k, v in self.clue_index.items():
            if k in self.hidden_clues:
                value = 1
            else:
                value = 0
            clues[k] = v[value]
        return clues

    @property
    def time_to_open_clue(self):
        if not self.playtime or not self.hidden_clues:
            return False
        return bool(((self.playtime[0].total_seconds()/60)/len(self.hidden_clues)) < self.open_clue_interval)

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
        self.hidden_clues = self.clue_index.keys()

    def _add_clue(self, clue_name, clue):
        self.clue_index[clue_name] = [clue, 'HIDDEN']

    def open_next_clue(self):
        if self.hidden_clues:
            reveal = self.hidden_clues.pop()
            return reveal

    def jsonify(self):
        return {
            'time': self.playtime[1],
            'guesses': self.latest_guess,
            'clues': self.clues}

    def generate_room_id(self):
        self.room_id = ''.join(random.SystemRandom().choice(
                        string.ascii_uppercase) for _ in range(current_app.config['ROOM_ID_LENGTH']))

    def end_game(self):
        while self.hidden_clues:
            self.open_next_clue()

