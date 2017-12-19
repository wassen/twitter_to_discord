#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import html
import requests
from requests_oauthlib import OAuth1  # ,OAuth1Session
from typing import Dict, List


class EnvironKeys:
    api_key             = "API_KEY"
    api_secret          = "API_SECRET"
    access_token        = "ACCESS_TOKEN"
    access_secret       = "ACCESS_SECRET"
    twitter_id          = "TWITTER_ID"
    discord_webhook_url = "DISCORD_WEBHOOK_URL"


def postToDiscord(content       : str,
                  username      : str,
                  image_url     : str,
                  media_url_list: List[str]):
    requests.post(
        url=os.environ[EnvironKeys.discord_webhook_url],
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "content"   : content,
            "username"  : username,
            "avatar_url": image_url,
            "embeds"     : [{"image": {"url": media_url}} for media_url in media_url_list],
        }),
    )


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
        # TODO: log posted tweet and unexpected error
        try:
            serialized_tweet: dict = json.loads(tweet)
            # type sage serialize
            if not str(serialized_tweet["user"]["id"]) == os.environ[EnvironKeys.twitter_id]:
                print("others")
                continue

            tweet_text     : str       = html.unescape(serialized_tweet["text"])
            tweet_username : str       = serialized_tweet["user"]["name"]
            tweet_image_url: str       = serialized_tweet["user"]["profile_image_url"]
            media_url_list : List[str] = [media["media_url"] for media in serialized_tweet["entities"].get("media", [])]

            for media_url2 in [media["url"] for media in serialized_tweet["entities"].get("media", [])]:
                tweet_text: str = tweet_text.replace(media_url2, "")

            postToDiscord(
                content       =tweet_text,
                username      =tweet_username,
                image_url     =tweet_image_url,
                media_url_list=media_url_list,
            )
            print(tweet_text)
        except json.decoder.JSONDecodeError:
            print(tweet)
        except:
            print("unexpected")
            print(tweet)
