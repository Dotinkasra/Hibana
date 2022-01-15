import sqlite3
from typing import Iterable

class Controller():
    def __init__(self) -> None:
        self.dbname = 'hibana/data/data.db'
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()
        self.cur.execute(
            f'CREATE TABLE IF NOT EXISTS token(userid TEXT PRIMARY KEY, access_token TEXT NOT NULL, access_token_secret TEXT NOT NULL)'
        )
        self.conn.commit()
        self.__close()

    def __connect(self) -> None:
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def __close(self):
        self.conn.close()

    def set_token(self, userid: str, access_token: str, access_token_secret: str):
        self.__connect()
        self.cur.execute(
            'INSERT INTO token (userid, access_token, access_token_secret) VALUES (?, ?, ?)',
            (userid, access_token, access_token_secret)
        )
        self.conn.commit()
        self.__close()

    def update_token(self, userid: str, access_token: str, access_token_secret: str):
        self.__connect()
        self.cur.execute(
            f'UPDATE token set access_token = ?, access_token_secret = ? WHERE userid = ?',
            (access_token, access_token_secret, userid)
        )
        self.conn.commit()
        self.__close()

    def get_access_token(self, userid: str) -> list:
        self.__connect()
        self.cur.execute(
            'SELECT * FROM token WHERE userid = ?',
            (userid,)
        )
        result: list = self.cur.fetchall()
        self.__close()
        return result

