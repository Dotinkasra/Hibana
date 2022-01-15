from datetime import datetime

class User():
    _id: str 
    _location: str 
    _nickname: str
    _username: str
    _profile_image_url: str
    _created_at: datetime

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, val):
        self._location = val

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, val):
        self._nickname = val

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, val):
        self._username = val

    @property
    def profile_image_url(self):
        return self._profile_image_url
    
    @profile_image_url.setter
    def profile_image_url(self, val):
        self._profile_image_url = val

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, val):
        self._created_at = val