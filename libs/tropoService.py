import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class TropoService:

    def __init__(self, logger):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.logger = logger
        self.host = 'https://api.tropo.com'
        self.token = '098fabd34cc5fb448571f12b4d1573b43774be7d8634c67b5dbef6c942e5f7fd92075777dd57d73879d925ae'
        self.reqSession = requests.Session()
        self.reqSession.headers.update({'Content-Type': 'application/json'})

    def sendMessages(self, message, phoneNumbers):
        messageUrl = self.host + '/1.0/sessions?action=create&token=' + self.token + '&msg=' + message + ' &numberToDial='
        for phoneNumber in phoneNumbers:
            self.reqSession.get(messageUrl + phoneNumber, verify=False)
