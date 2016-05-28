#!/usr/local/bin/python3
import requests
from urllib.parse import quote_plus

baseUrl = 'http://ciscohackathon2016.cloudapp.net:5000'


def deleteData(url):
    resp = requests.delete(baseUrl + url)
    if resp.status_code != 204:
        raise Exception('Delete to ' + url + ' returned a status of ' + str(resp.status_code) + ' ' + resp.text)

roomName = "hackathon2016"
members = [{"personEmail": "todd.erickson@wwt.com"}, {"personEmail": "derek.lohman@wwt.com"}, {"personEmail": "shawn.donoho@wwt.com>"}, {"personEmail": "tim.fuller@asynchrony.com"}, {"personEmail": "Dave.Guidos@asynchrony.com"}]
webhookName = "hackathonHook"

deleteData('/webhooks/' + webhookName)
for member in members:
    memberUrl = '/rooms' + '/' + roomName + '/members/' + quote_plus(member['personEmail'])
    deleteData(memberUrl)
deleteData('/rooms/' + roomName)
