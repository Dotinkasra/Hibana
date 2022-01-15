from datetime import datetime
from hibana.schemas.user import User
from hibana.schemas.media import Media

class ATweet():
    _id: str
    _lang: str
    _created_at: datetime
    _media: list[Media]
    _user: User

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def lang(self):
        return self._lang

    @id.setter
    def lang(self, val):
        self._lang = val

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, val):
        self._created_at = val

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, val):
        self._user = val

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, val):
        self._media = val

