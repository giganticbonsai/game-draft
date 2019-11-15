import random

from flask import url_for


class Guess(object):

    def __init__(self, answer):
        self.answer = str(answer).upper()
        self.clues = {}
        self.hidden_clues = []
        self.guessed = False
        self.scrambled = self._partial_answer()

    @property
    def display_name(self):
        if self.guessed:
            return self.answer
        return self.scrambled

    def is_answer(self, guess):
        return guess.strip().lower() == self.answer.strip().lower()

    def _load_clues(self):
        self.hidden_clues = self.clues.keys()

    def _add_clue(self, clue_name, clue, hidden_value='HIDDEN'):
        self.clues[clue_name] = [clue, hidden_value]

    def open_next_clue(self):
        if self.hidden_clues:
            reveal = self.hidden_clues.pop()
            return reveal

    def _scramble_answer(self):
        words = self.answer.split()
        scrambled = []
        for w in words:
            scrambled.append(''.join(random.sample(list(w), len(w))))
        random.shuffle(scrambled)
        return ' '.join(scrambled)

    def _partial_answer(self):
        inds = [i for i, _ in enumerate(self.answer) if not _.isspace()]
        num_to_replace = int(len(inds)*0.75)
        sam = random.sample(inds, num_to_replace)
        partial = list(self.answer)
        for idx in sam:
            partial[idx] = '-'
        return ''.join(partial)


class Song(Guess):

    def __init__(self, spotify_manager, title, artist=None):
        super(Song, self).__init__(title)
        self.spotify = spotify_manager

        self._init_song(title, artist)
        self._add_artist_clue()
        self._add_album_clue()
        self._load_clues()

    def _init_song(self, title, artist):
        tracks = self.spotify.search_track(title)
        idx = 0
        artist_id = tracks[0]['artists'][0]['id']
        if artist:
            for count, t in enumerate(tracks):
                if t['name'].lower() == title.lower() and t['artists'][0]['name'].lower() == artist.lower():
                    idx = count
                    artist_id = t['artists'][0]['id']
                    break
        self.artist = self.spotify.get_artist(artist_id)
        self.track = tracks[idx]
        self.album = tracks[idx]['album']


    @property
    def info(self):
        pass

    def _add_artist_clue(self):
        artist_clue = {
            'value': self.artist['name'],
            'image': self._get_image_url(self.artist['images'])
        }
        hidden_value = {
            'value': 'Artist',
            'image': url_for('static', filename='images/hidden_clue.png')
        }
        self._add_clue('Artist', artist_clue, hidden_value)

    def _add_album_clue(self):
        album_clue = {
            'value': self.album['name'],
            'image': self._get_image_url(self.album['images'])
        }
        hidden_value = {
            'value': 'Album',
            'image': url_for('static', filename='images/hidden_clue.png')
        }
        self._add_clue('Album', album_clue, hidden_value)

    def _get_image_url(self, image_list):
        for i in range(len(image_list)):
            if 'url' in image_list[i]:
                return image_list[i]['url']
        return None
