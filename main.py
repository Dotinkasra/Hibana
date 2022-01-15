import tweepy
from flask import Flask, request, render_template
from hibana.module.oauth import Oauth
from hibana.module.db import Controller
from hibana.env.config import Config

config = Config()
controller = Controller()

class Main():
    def __init__(self) -> None:
        token = controller.get_access_token(config.userid)
        if token is None or len(token) <= 0:
            oauth = Oauth()
            oauth.main()
        else:
            self.client = tweepy.Client(
                bearer_token = config.bearer_token, 
                consumer_key = config.api_key, 
                consumer_secret = config.api_secret_key, 
                access_token = token[0][1],
                access_token_secret = token[0][2]
            )

    def timeline(self, count: int = 5):
        
        print(
            self.client.get_users_tweets(
                id = config.userid,
                user_auth = True,
                max_results = count
            )
        )

    def tweet(self, text):
        self.client.create_tweet(text=text)

main = Main()
main.timeline()