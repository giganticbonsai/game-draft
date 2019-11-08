import base64
import json
import os
from datetime import datetime, timedelta

import requests


class SpotifyCredentials(object):
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id=None, client_secret=None, proxies=None):

        if not client_id:
            client_id = os.environ.get('SPOTIFY_ID')

        if not client_secret:
            client_secret = os.environ.get('SPOTIFY_SECRET')

        if not proxies:
            proxies = {
                "http": os.environ.get('http_proxy'),
                "https": os.environ.get('http_proxy'),
                "no_proxy": os.environ.get('no_proxy'),
            }

        self.client_id = client_id
        self.client_secret = client_secret
        self.proxies = proxies

        self._request_auth_token()

    @property
    def auth_token(self):
        if self._is_token_expired():
            self._request_auth_token()
        return self.auth_details["access_token"]

    def _get_auth_header(self):
        encoded_bytes = base64.urlsafe_b64encode('{}:{}'.format(self.client_id, self.client_secret).encode("utf-8"))
        encoded_str = str(encoded_bytes)
        return {"Authorization": "Basic {}".format(encoded_str)}

    def _request_auth_token(self):
        payload = {'grant_type': 'client_credentials'}
        req_time = datetime.utcnow()
        resp = requests.post('https://accounts.spotify.com/api/token',
                             headers=self._get_auth_header(),
                             data=payload,
                             verify=True,
                             proxies=self.proxies)
        if resp.status_code == 200:
            self.auth_details = json.loads(resp.text)
            self.auth_details['time_requested'] = req_time

    def _is_token_expired(self):
        if not self.auth_details or (datetime.utcnow() - self.auth_details['time_requested']) >=\
                timedelta(seconds=self.auth_details['expires_in']):
            return True
        return False


