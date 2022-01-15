from ctypes import Union
from urllib import request, response
import tweepy
from hibana.module.db import Controller
from hibana.env.config import Config
from hibana.module.oauth import Oauth
from hibana.schemas.media import Media
from hibana.schemas.tweet import ATweet
from hibana.schemas.user import User

controller = Controller()
config = Config()

class Twitter():
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

    def tweet(self, **kwargs):
        self.client.create_tweet(**kwargs)

    def info_tweet_id(self, tweetid: str = '1463972011013652485'):
        return self.client.get_tweet(
            id = tweetid,
            user_auth = True,
            expansions = ['author_id', 'attachments.media_keys', 'referenced_tweets.id', 'entities.mentions.username', 'referenced_tweets.id.author_id'],
            tweet_fields = ['created_at', 'lang', 'entities', 'geo'],
            user_fields = ['created_at', 'description', 'entities', 'id', 'location', 'name', 'profile_image_url', 'username', 'verified']
        )

    def get_tweet(self, response: Union) -> ATweet:
        if len(response.errors) >= 1:
            return response.errors
        
        tweet = ATweet()
        tweet.id = response.data.id
        tweet.lang = response.data.lang
        tweet.created_at = response.data.created_at

        if 'users' in response.includes:
            user = User()
            user.id = response.includes['users'][0].id
            user.location = response.includes['users'][0].location
            user.nickname = response.includes['users'][0].name
            user.username = response.includes['users'][0].username
            user.profile_image_url = response.includes['users'][0].profile_image_url
            tweet.user = user

        if 'media' in response.includes:
            tweet.media = []
            for contents in response.includes['media']:
                media = Media()
                media._media_key = contents.media_key
                media._type = contents.type
                tweet.media.append(media)
