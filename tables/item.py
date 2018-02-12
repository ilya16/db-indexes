class Item(object):
    """Item class that contains two fields: key and data"""
    def __init__(self, _key, _data):
        self._key = _key
        self._data = _data

    def key(self):
        return self._key

    def value(self):
        return self._data
