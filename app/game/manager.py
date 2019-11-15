from __future__ import division
import random
import string
from datetime import datetime, timedelta

from flask import current_app

from app.game.song import Song


class Manager(object):

    NUMBER_OF_GUESSES_SHOWN = 10

    def __init__(self, song, artist, spotify_manager, duration=5):
        self.room_id = 0
        self.players = []
        self.spotify = spotify_manager

        self.generate_room_id()
        self._start_game(song, artist, duration)

    def _start_game(self, song, artist, duration):
        self.date_end = datetime.utcnow() + timedelta(minutes=duration)
        self.song = Song(self.spotify, song, artist)
        self.guesses = [''] * self.NUMBER_OF_GUESSES_SHOWN
        self.open_clue_interval = duration/(len(self.song.hidden_clues)+1)

    @property
    def playtime(self):
        td = self.date_end - datetime.utcnow()
        time_since = divmod(td.days*86400 + td.seconds, 60)
        time_str = '{0} minutes, {1:02d} seconds'.format(time_since[0], time_since[1])
        if self.date_end <= datetime.utcnow():
            time_str = '00:00'
        return [td, time_str]

    @property
    def latest_guess(self):
        return self.guesses[0:self.NUMBER_OF_GUESSES_SHOWN]

    @property
    def clues(self):
        clues = {}
        for k, v in self.song.clues.items():
            if k in self.song.hidden_clues:
                value = 1
            else:
                value = 0
            clues[k] = v[value]
        return clues

    @property
    def time_to_open_clue(self):
        if not self.playtime or not self.song.hidden_clues:
            return False
        return bool(((self.playtime[0].total_seconds()/60)/len(self.song.hidden_clues)) < self.open_clue_interval)

    def add_player(self, name):
        self.players.append(name)

    def remove_player(self, name):
        self.players.remove(name)

    def is_song(self, guess):
        if self.song.is_answer(guess):
            self.end_game()
            return True
        self.guesses.insert(0, guess)
        return False

    def jsonify(self):
        return {
            'song': self.song.display_name,
            'time': self.playtime[1],
            'guesses': self.latest_guess,
            'clues': self.clues}

    def generate_room_id(self):
        self.room_id = ''.join(random.SystemRandom().choice(
                        string.ascii_uppercase) for _ in range(current_app.config['ROOM_ID_LENGTH']))

    def end_game(self):
        self.song.guessed = True
        while self.song.hidden_clues:
            self.song.open_next_clue()



