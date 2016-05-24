import json
from types import MethodType


def methodize(func, instance):
    return MethodType(func, instance)


class Membership(object):
    def _instance_url(self, id):
        return '/memberships/{}'.format(self.id)

    def __init__(self, attributes=None):

        if attributes:
            self.attributes = attributes

        else:
            self.attributes = dict()
            self.attributes['id'] = None
            self.attributes['roomId'] = None
            self.attributes['personId'] = None
            self.attributes['personEmail'] = None
            self.attributes['isModerator'] = None
            self.attributes['isMonitor'] = None
            self.attributes['created'] = None

        if self.attributes['id']:
            # Override classmethod if id is set
            self.url = methodize(self._instance_url, self)

    @classmethod
    def url(self):
        return '/memberships'

    @property
    def created(self):
        return self.attributes['created']

    @created.setter
    def created(self, val):
        self.attributes['created'] = val

    @property
    def roomId(self):
        return self.attributes['roomId']

    @roomId.setter
    def roomId(self, val):
        self.attributes['roomId'] = val

    @property
    def id(self):
        return self.attributes['id']

    @id.setter
    def id(self, val):
        self.attributes['id'] = val

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
    def isModerator(self):
        return self.attributes['isModerator']

    @isModerator.setter
    def isModerator(self, val):
        self.attributes['isModerator'] = val

    @property
    def isMonitor(self):
        return self.attributes['isMonitor']

    @isMonitor.setter
    def isMonitor(self, val):
        self.attributes['isMonitor'] = val

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
    def find(cls, session, roomId=None, personId=None):
        """
        Retrieve a room or persons memberships
        :param session: Session object
        :return: membership or list of membership objects
        """
        if (roomId is None) and (personId is None):
            raise ValueError('must specify either name or email')
        else:
            if roomId:
                query = 'roomId'
                value = roomId
            if personId:
                query = 'personId'
                value = personId
            url = cls.url() + '?{}={}'.format(query, value)
            resp = session.get(url)
            items = json.loads(resp.text)['items']
            if len(items) == 1:
                obj = cls.from_json(items[0])
                ret = obj
            elif len(items) > 1:
                ret = []
                for i in items:
                    obj = cls.from_json(i)
                    ret.append(obj)
            return ret

    def create(self, session):
        url = self.url()
        resp = session.post(url, self.json())
        #update attributes after creating
        data = resp.json()
        self.id = data['id']
        self.created = data['created']
        return resp

    def delete(self, session):
        url = self.url()
        resp = session.delete(url)
        return resp
