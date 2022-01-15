class Media():
    _media_key: str = None
    _type: str = None

    @property
    def media_key(self):
        return self._media_key

    @media_key.setter
    def media_key(self, val: str):
        self._media_key = val

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val: str):
        self._type = val
