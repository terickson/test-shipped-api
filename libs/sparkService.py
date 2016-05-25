from spark.rooms import Room
from spark.session import Session
from spark.webhooks import Webhook
from spark.people import Person
from spark.membership import Membership
from libs.restException import RestException
from spark.messages import Message


class SparkService:

    def __init__(self, logger):
        self.logger = logger
        url = 'https://api.ciscospark.com'
        #Token for beekeeperbot@gmail.com password ATC usual
        token = 'OGQxYmU4MjQtNTUxOS00ODA5LWI1YTItYTUyZWM2ZTAxZjE1OGMxNDU1YWEtNGNj'
        self.session = Session(url, token)

    def getRooms(self):
        rooms = Room.get(self.session)
        return rooms

    def createRoom(self, roomname):
        room = Room()
        room.title = roomname
        room.create(self.session)
        return room

    def getRoom(self, roomname):
        return Room.get(self.session, name=roomname)

    def deleteRoom(self, roomname):
        room = self.getRoom(roomname)
        room.delete(self.session)

    def createMessage(self, roomname, messageTxt):
        room = Room.get(self.session, name=roomname)
        resp = room.send_message(self.session, messageTxt)
        if resp.status_code != 200 and resp.status_code != 201:
            raise RestException(resp.text, resp.status_code)

    def getRoomMessages(self, roomname):
        room = Room.get(self.session, name=roomname)
        msgs = room.get_messages(self.session)
        return msgs

    def createRoomWebhook(self, roomname, webhookUrl, webhookName):
        webhook = Webhook()
        room = Room.get(self.session, name=roomname)
        webhook.set_targetUrl(webhookUrl)
        webhook.set_filter('roomId={}'.format(room.id))
        webhook.set_name(webhookName)
        webhook.set_resource('messages')
        webhook.set_event('created')
        webhook.create(self.session)
        return webhook

    def getMessage(self, messageId):
        return Message.get(self.session, messageId)

    def getWebhooks(self):
        return Webhook.get(self.session)

    def getWebhook(self, webhookName):
        webhooks = self.getWebhooks()
        for webhook in webhooks:
            if webhook.get_name() == webhookName:
                return webhook
        return None

    def deleteWebhook(self, webhookName):
        webhook = self.getWebhook(webhookName)
        if webhook:
            webhook.delete(self.session)

    def getPersonByEmail(self, userEmail):
        return Person.find(self.session, email=userEmail)

    def getRoomMembers(self, roomname):
        room = self.getRoom(roomname)
        return Membership.find(self.session, roomId=room.id)

    def createRoomMembers(self, roomname, userEmail):
        membership = Membership()
        room = self.getRoom(roomname)
        person = self.getPersonByEmail(userEmail)
        membership.roomId = room.id
        membership.personId = person.id
        membership.isModerator = 'false'
        membership.isMonitor = 'false'
        membership.create(self.session)
        return membership

    def getRoomMember(self, roomname, userEmail):
        members = self.getRoomMembers(roomname)
        person = self.getPersonByEmail(userEmail)
        if isinstance(members, list):
            for member in members:
                if member.personId == person.id:
                    return member
        return None

    def deleteRoomMember(self, roomname, userEmail):
        member = self.getRoomMember(roomname, userEmail)
        if member:
            member.delete(self.session)
