from lib2to3.pgen2 import token
from hibana.env.config import Config
from requests_oauthlib import OAuth1Session
config = Config()

class Oauth():

    def __init__(self) -> None:
        """
        コンストラクタ
        OAuth認証用のパラメタを取得する
        """
        self.requests_token: str = OAuth1Session(
            config.api_key, config.api_secret_key
        ).post(
            url = 'https://api.twitter.com/oauth/request_token',
            params = {'oauth_callback': 'http://localhost:5000'}
        ).text

    def get_requests_token(self, key: str) -> str:
        """パラメタ取得用メソッド

        Args:
            key (str): 取得したいパラメタのキーを入力(oauth_token, oauth_token_secret, oauth_callback_confirmed)

        Returns:
            str: 引数で与えられたキーの値
        """
        return {param.split('=')[0] : param.split('=')[1] for param in self.requests_token.split('&')}[key]

    def get_verify_url(self) -> str:
        """Verify用のURLを作成し返却するメソッド

        Returns:
            str: Verify用のURL
        """
        return f'https://api.twitter.com/oauth/authenticate?oauth_token={self.get_requests_token(key = "oauth_token")}'

    def get_access_token(self, oauth_verifier: str) -> str:
        """アクセストークンを取得するメソッド

        Args:
            oauth_verifier (str): Twitter連携後に得られるVerifierパラメタ

        Returns:
            str: 返却されたアクセストークン
        """
        return OAuth1Session(
            config.api_key, config.api_secret_key, self.get_requests_token(key = "oauth_token"), oauth_verifier
        ).post(
            'https://api.twitter.com/oauth/access_token',
            params = {'oauth_verifier' : oauth_verifier}
        ).text

    def save_access_token(self, verifier_result: str):
        """[summary]

        Args:
            verifier_result (str): 返却されたアクセストークン
        """
        params: dict = {param.split('=')[0] : param.split('=')[1] for param in verifier_result.split('&')}
        access_token = params['oauth_token']
        access_token_secret = params['oauth_token_secret']
        userid = params['user_id']
        screen_name = params['screen_name']

        print(f"access_token: {access_token}")
        print(f"access_token_secret : {access_token_secret}")
        print(f"userid : {userid}")
        print(f"screen name : {screen_name}")

        
    def main(self):
        print(self.get_verify_url())

        self.save_access_token(
            self.get_access_token(oauth_verifier = input())
        )
