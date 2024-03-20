import json
import random
from urllib import parse, request
from config import GIPHY_KEY, GIPHY_URL, GIPHY_LIMIT


# Interface to access Giphy service and get GIFs
class GiphyConnector:
    def __init__(self):
        self.params = {'otter': {
            "tag": "cute otter",
            "api_key": GIPHY_KEY,
        }, 'cat': {
            "tag": "cat",
            "api_key": GIPHY_KEY,
        }}

    def get_random_url(self, tag: str):
        with request.urlopen("".join((GIPHY_URL, "?", parse.urlencode(self.params[tag])))) as response:
            return json.loads(response.read())['data']['images']['original']['url']
