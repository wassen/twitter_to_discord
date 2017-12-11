#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import requests
from requests_oauthlib import OAuth1  # ,OAuth1Session


class EnvironKeys:
    api_key       = "API_KEY"
    api_secret    = "API_SECRET"
    access_token  = "ACCESS_TOKEN"
    access_secret = "ACCESS_SECRET"
    twitter_id    = "TWITTER_ID"


if __name__ == "__main__":
    oauth = OAuth1(
        os.environ[EnvironKeys.api_key],
        os.environ[EnvironKeys.api_secret],
        os.environ[EnvironKeys.access_token],
        os.environ[EnvironKeys.access_secret],
    )

    response = requests.post(
        url="https://stream.twitter.com/1.1/statuses/filter.json",
        auth=oauth,
        stream=True,
        data={"follow": os.environ[EnvironKeys.twitter_id]}
    )

    for tweet in response.iter_lines():
        try:
            print(json.loads(tweet)["text"])
        except json.decoder.JSONDecodeError:
            print(tweet)
