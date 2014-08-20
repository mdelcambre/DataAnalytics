#!/usr/bin/env python
"""Reads the Twitch API"""


from private_info import *
import json
from requests_oauthlib import OAuth2Session

# Global API url
url = 'https://api.twitch.tv/kraken'


twitch_api = json.loads(requests.get(url=url).text)

users = json.loads(requests.get(url=twitch_api['_links']['channel']).text)
