import configparser
import os

class Config():
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(path, 'UTF-8')

    @property
    def api_key(self) -> str:
        return str(self.config['KEYS']['api_key'])

    @property
    def api_secret_key(self) -> str:
        return str(self.config['KEYS']['api_secret_key'])

    @property
    def bearer_token(self) -> str:
        return str(self.config['KEYS']['bearer_token'])

    @property
    def access_token(self) -> str:
        return str(self.config['KEYS']['access_token'])

    @property
    def access_token_secret(self) -> str:
        return str(self.config['KEYS']['access_token_secret'])

    @property
    def userid(self) -> str:
        return str(self.config['ID']['my_id'])