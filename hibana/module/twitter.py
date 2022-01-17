from ctypes import Union
from pydoc import text
from urllib import request, response
import tweepy

from hibana.env.config import Config
from hibana.module.db import Controller
from hibana.module.oauth import Oauth
from hibana.schemas.media import Media
from hibana.schemas.tweet import ATweet
from hibana.schemas.user import User
from hibana.schemas.timeline import Timeline

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

    def info_user_id(self, id: str) -> tweepy.User:
        return self.client.get_user(
            id = id,
            user_auth = True,
            user_fields = ['created_at', 'description', 'protected', 'id', 'url', 'name', 'profile_image_url', 'username']
        ).data

    def info_username(self, username: str) -> tweepy.User:
        return self.client.get_user(
            username = username,
            user_auth = True,
            user_fields = ['created_at', 'description', 'protected', 'id', 'url', 'name', 'profile_image_url', 'username']
        ).data

    def info_tweet_id(self, id: str):
        return self.client.get_tweet(
            id = id,
            user_auth = True,
            expansions = ['author_id', 'attachments.media_keys', 'referenced_tweets.id', 'referenced_tweets.id.author_id'],
            tweet_fields = ['created_at', 'conversation_id', 'source'],
            user_fields = ['created_at', 'description', 'entities', 'id', 'location', 'name', 'profile_image_url', 'username', 'verified']
        )

    def __get_timeline(self, id: str, next_token: str = None) -> tweepy.Response:
        if next_token:
            return self.client.get_users_tweets(
                id = id,
                user_auth = True,
                max_results = 6,
                pagination_token = next_token,
                expansions = ['author_id', 'referenced_tweets.id.author_id'],
                tweet_fields = ['created_at', 'conversation_id', 'source']
            )
        else:
            return self.client.get_users_tweets(
                id = id,
                user_auth = True,
                max_results = 6,
                expansions = ['author_id', 'referenced_tweets.id.author_id'],
                tweet_fields = ['created_at', 'conversation_id', 'source']
            )

    def timeline(self, **kwargs):
        #self.display_tweet(self.get_tweet_obj(self.__get_timeline()))
        res: tweepy.Response = self.__get_timeline(**kwargs)
        tweets = {x.id: x for x in res.data}
        #sub_tweets = [] if 'tweets' not in res.includes else [x for x in res.includes['tweets']]
        sub_tweets = {} if 'tweets' not in res.includes else {x.id: x for x in res.includes['tweets']}
        for t in tweets.items():
            author = self.info_user_id(t[1].author_id)
            print('--------------------')
            if t[1].referenced_tweets:
                if t[1].referenced_tweets[0]["type"] == 'retweeted':
                    print(f'{author.name}さんが{t[1].created_at}にリツイート')
                    print(f'{t[1].source}\n')
                    original = self.info_user_id(sub_tweets[t[1].referenced_tweets[0]['id']].author_id)
                    print(f'{original.name}@{original.username}\n')
                    print(f'{t[1].text}\n')
                    print(f'{t[1].created_at}\t{t[1].source}')
                if t[1].referenced_tweets[0]["type"] == 'replied_to':
                    print(f'{author.name}さんがリプライ\n')
                    original = self.info_user_id(sub_tweets[t[1].referenced_tweets[0].id].author_id)
                    print(f'{original.name}@{original.username}')
                    print(f'{sub_tweets[t[1].referenced_tweets[0].id].text}\n')
                    print(f'{sub_tweets[t[1].referenced_tweets[0].id].created_at}\t{sub_tweets[t[1].referenced_tweets[0].id].source}')
                    print('⤴')
                    print(f'{author.name}@{author.username}\n')
                    print(f'{t[1].text}\n')
                    print(f'{t[1].created_at}\t{t[1].source}')
            else:
                print(f'{author.name}@{author.username}\n')
                print(f'{t[1].text}\n')
                print(f'{t[1].created_at}\t{t[1].source}')         
        
        print('Show next page?(y/n)')
        if input() == 'y':
            self.timeline(id = kwargs['id'], next_token =res.meta['next_token'])
        

            

    def display_tweet(self, tweets: list[ATweet]):
        for t in tweets:
            print('--------------------')
            print(f'{t.user.name}@{t.user.username}\n')
            print(f'{t.tweet.text}')
            print(f'{t.tweet.created_at}')

    def like(self):
        pass

    def dislike(self):
        pass

    def retweet(self):
        pass

    def get_tweet_obj(self, response: Union) -> ATweet:
        if len(response.errors) >= 1:
            return response.errors

        data = [x for x in response.data] if type(response.data) == list else [response.data]
        tweets = []
        for t in data:
            tweet = ATweet()
            for u in response.includes['users']:
                if t.author_id == u.id:
                    tweet.tweet = t
                    tweet.user = u
                    tweets.append(tweet)
                else:
                    continue
        return tweets
        #tweets: list[ATweet] = [self.__create_tweet(t) for t in response.data] if type(response.data) == list else [self.__create_tweet(response.data)]
        #users: list[User] = [self.__create_user(u) for u in list(response.includes['users'])] 
        #return [tweets, users]
