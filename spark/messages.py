import json
from pprint import pprint


class Message(object):
    def __init__(self, attributes=None):
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = dict()
            self.attributes['id'] = None
            self.attributes['text'] = None
            self.attributes['roomId'] = None
            self.attributes['personId'] = None
            self.attributes['personEmail'] = None
            self.attributes['created'] = None

    @property
    def id(self):
        return self.attributes['id']

    @id.setter
    def id(self, val):
        self.attributes['id'] = val

    @property
    def text(self):
        return self.attributes['text']

    @text.setter
    def text(self, val):
        self.attributes['text'] = val

    @property
    def roomId(self):
        return self.attributes['roomId']

    @roomId.setter
    def roomId(self, val):
        self.attributes['roomId'] = val

    @property
    def personId(self):
        return self.attributes['personId']

    @personId.setter
    def personId(self, val):
        self.attributes['personId'] = val

    @property
    def personEmail(self):
        return self.attributes['personEmail']

    @personEmail.setter
    def personEmail(self, val):
        self.attributes['personEmail'] = val

    @property
    def created(self):
        return self.attributes['created']

    @created.setter
    def created(self, val):
        self.attributes['created'] = val

    def json(self):
        return json.dumps(self.attributes)

    @classmethod
    def from_json(cls, obj):
        if isinstance(obj, dict):
            obj = cls(attributes=obj)
        elif isinstance(obj, (str, unicode)):
            obj = cls(attributes=json.loads(obj))
        else:
            raise TypeError('Data must be str or dict')
        return obj

    @classmethod
    def url(cls, id=None):
        url = '/messages'
        if id:
            url + '/' + str(id)
        return url

    @classmethod
    def get(cls, session, id=None):
        ret = []
        messages = json.loads(session.get(cls.url(id)).text)
        pprint(messages)
        if not isinstance(messages, list):
            return cls.from_json(messages)
        for message in messages:
            obj = cls.from_json(message)
            ret.append(obj)
        return ret
