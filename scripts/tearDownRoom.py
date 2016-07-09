#!/usr/local/bin/python3
import requests
from urllib.parse import quote_plus

baseUrl = 'http://ciscohackathon2016.cloudapp.net:5000'


def deleteData(url):
    resp = requests.delete(baseUrl + url)
    if resp.status_code != 204:
        raise Exception('Delete to ' + url + ' returned a status of ' + str(resp.status_code) + ' ' + resp.text)

rooms = [{"title": "hackathon2016", "webhookName": "hackathonHook"}, {"title": "global", "webhookName": "globalHook"}, {"title": "local", "webhookName": "localHook"}]
members = [{"personEmail": "todd.erickson@wwt.com"}, {"personEmail": "derek.lohman@wwt.com"}, {"personEmail": "shawn.donoho@wwt.com"}, {"personEmail": "tim.fuller@asynchrony.com"}, {"personEmail": "dave.guidos@asynchrony.com"}]

for roomData in rooms:
    deleteData('/webhooks/' + roomData['webhookName'])
    for member in members:
        memberUrl = '/rooms' + '/' + roomData['title'] + '/members/' + quote_plus(member['personEmail'])
        deleteData(memberUrl)
    deleteData('/rooms/' + roomData['title'])
