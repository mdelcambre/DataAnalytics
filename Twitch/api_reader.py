#!/usr/bin/env python
"""Reads the Twitch API"""


import json
import requests
from sets import Set

# Global API url
url = 'https://api.twitch.tv/kraken'
header = {"Accept":"application/vnd.twitchtv.v2+json","Client-ID":r'nxdcczxegqz6miyg9b5br2nav2col3c'}


twitch_api = json.loads(requests.get(url=url,headers=header).text)


streams = Set()

responses = []
responses.append(json.loads(requests.get(url=twitch_api['_links']['streams']+'?limit=100',headers=header).text))
for i in range(0,10):
    responses.append(json.loads(requests.get(url=responses[i]['_links']['next'],headers=header).text))
for response in responses:
    for channel in response['streams']:
        stream = channel['channel']['name']
        if stream not in streams:
            streams.add(stream)

print(streams)
print(len(streams))
