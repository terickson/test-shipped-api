import json
from types import MethodType


def methodize(func, instance):
    return MethodType(func, instance)


class Person(object):
    def _instance_url(self, id):
        return '/people/{}'.format(self.id)

    def __init__(self, attributes=None):

        if attributes:
            self.attributes = attributes

        else:
            self.attributes = dict()
            self.attributes['created'] = None
            self.attributes['displayName'] = None
            self.attributes['id'] = None
            self.attributes['avatar'] = None
            self.attributes['emails'] = None

        if self.attributes['id']:
            # Override classmethod if id is set
            self.url = methodize(self._instance_url, self)

    @classmethod
    def url(cls):
        return '/people'

    @property
    def created(self):
        return self.attributes['created']

    @created.setter
    def created(self, val):
        self.attributes['created'] = val

    @property
    def displayName(self):
        return self.attributes['displayName']

    @displayName.setter
    def set_displayName(self, val):
        self.attributes['displayName'] = val

    @property
    def id(self):
        return self.attributes['id']

    @id.setter
    def id(self, val):
        self.attributes['id'] = val

    @property
    def avatar(self):
        return self.attributes['avatar']

    @avatar.setter
    def avatar(self, val):
        self.attributes['avatar'] = val

    @property
    def emails(self):
        return self.attributes['emails']

    @emails.setter
    def emails(self, val):
        self.attributes['emails'] = val

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
    def find(cls, session, name=None, email=None):
        """
        Retrieve a person by Display name or email
        :param session: Session object
        :return: person or list of person objects
        """
        if (name is None) and (email is None):
            raise ValueError('must specify either name or email')
        else:
            if name:
                query = 'displayName'
                value = name
            if email:
                query = 'email'
                value = email
            url = cls.url() + '?{}={}'.format(query, value)
            resp = session.get(url)
            items = json.loads(resp.text)['items']
            ret = None
            if len(items) == 1:
                obj = cls.from_json(items[0])
                ret = obj
            elif len(items) > 1:
                ret = []
                for i in items:
                    obj = cls.from_json(i)
                    ret.append(obj)
            return ret
