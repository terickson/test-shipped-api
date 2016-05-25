ciscoHackathon2016.cloudapp.net

# test-shipped-api
POST http://0.0.0.0:5000/actions
Content-Type: application/json

{"type":"tropo",
"phoneNumbers": ["15209756399"],
"message":"This is a test"
}

{"type":"spark",
"roomname": "hackathon2016",
"message":"This is a test"
}

POST http://0.0.0.0:5000/rooms
Content-Type: application/json

{"title":"hackathon2016"}

POST http://0.0.0.0:5000/rooms/spark%20test%20room/members
Content-Type: application/json

{"personEmail":"todd.erickson@wwt.com"}

POST http://0.0.0.0:5000/webhooks
Content-Type: application/json

{
"roomname":"hackathon2016",
"url":"https://www.wwt.com/", 
"name": "testHook"
}