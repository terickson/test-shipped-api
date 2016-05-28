#!/usr/local/bin/python3
import requests
import json

baseUrl = 'http://ciscohackathon2016.cloudapp.net:5000'


def postData(url, data):
    resp = requests.post(baseUrl + url, data=json.dumps(data), headers={"content-type": "application/json"})
    if resp.status_code != 201:
        raise Exception('Post to ' + url + ' returned a status of ' + str(resp.status_code) + ' ' + resp.text)

roomData = {"title": "hackathon2016"}
members = [{"personEmail": "todd.erickson@wwt.com"}, {"personEmail": "derek.lohman@wwt.com"}, {"personEmail": "shawn.donoho@wwt.com>"}, {"personEmail": "tim.fuller@asynchrony.com"}, {"personEmail": "Dave.Guidos@asynchrony.com"}]
webhookData = {"roomname": roomData['title'], "url": baseUrl + "/alerts", "name": "hackathonHook"}

postData('/rooms', roomData)
for member in members:
    postData('/rooms' + '/' + roomData['title'] + '/members', member)
postData('/webhooks', webhookData)
