import json
import os
from pprint import pprint

import requests


class Spotify(object):
    trace = False
    max_retries = 10
    requests_timeout = 30
    url_prefix = 'https://api.spotify.com/v1/'

    def __init__(self, credentials_manager, proxies=None):
        self.credentials_manager = credentials_manager
        self._session = requests.Session()

        if not proxies:
            proxies = {
                "http": os.environ.get('http_proxy'),
                "https": os.environ.get('http_proxy'),
                "no_proxy": os.environ.get('no_proxy'),
            }
        self.proxies = proxies

    def _request_headers(self):
        token = self.credentials_manager.auth_token
        return {'Authorization': 'Bearer {0}'.format(token),
                'Content-Type': 'application/json'}

    def _request(self, method, endpoint, payload, params):
        args = dict(params=params)
        args["timeout"] = self.requests_timeout
        if payload:
            args["data"] = json.dumps(payload)

        resp = self._session.request(method,
                                     self.url_prefix+endpoint,
                                     headers=self._request_headers(),
                                     proxies=self.proxies,
                                     **args)
        return json.loads(resp.text)

    def _get(self, endpoint, args=None, payload=None, **kwargs):
        if args:
            kwargs.update(args)
        return self._request('GET', endpoint, payload, kwargs)

    def search_track(self, track):
        resp = self._get('search',
                         q=track,
                         limit=10,
                         offset=0,
                         type='track',
                         market=None)
        return resp['tracks']['items']

    def get_track(self, track):
        return self._get('tracks/?ids='+track,
                         market=None)






