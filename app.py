import traceback
import simplejson as json
import logging
from flask import Flask, request, Response
from flask.ext.cors import CORS
from libs.restException import RestException
from flask_socketio import SocketIO, emit
from libs.tropoService import TropoService
from libs.sparkService import SparkService
from uuid import uuid4

app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app)
actions = []
alerts = []
tropo = TropoService(logging)
spark = SparkService(logging)


def sparkJsonSafe(valObj):
    if isinstance(valObj, list):
        returnArray = []
        for val in valObj:
            returnArray.append(val.attributes)
        return returnArray
    else:
        return valObj.attributes


@app.errorhandler(Exception)
def exception_handler(e):
    if type(e) is RestException:
        return Response(e.message, mimetype='text/html'), e.statusCode
    tb = traceback.format_exc()
    logging.error(tb)
    return Response(e.message, mimetype='text/html'), 500


@app.route("/")
def hello():
    return "Welcome to the Hackathon API"


# base route for getting the actions
@app.route('/actions', methods=['GET'])
def get_actions():
    return Response(json.dumps(actions), mimetype='application/json')


# route to create an action
@app.route('/actions', methods=['POST'])
def create_action():
    action = request.json
    if action['type'] == 'tropo':
        tropo.sendMessages(action['message'], action['phoneNumbers'])
    elif action['type'] == 'spark':
        spark.createMessage(action['roomname'], action['message'])
    action['id'] = str(uuid4())
    logging.error(action)
    actions.append(action)
    return Response(json.dumps(action), mimetype='application/json'), 201


# base route for getting the alerts
@app.route('/alerts', methods=['GET'])
def get_alerts():
    return Response(json.dumps(sparkJsonSafe(alerts)), mimetype='application/json')


# route to create an action
@app.route('/alerts', methods=['POST'])
def create_alert():
    envelope = request.json
    alert = spark.getMessage(envelope['data']['id'])
    alerts.append(alert)
    return Response(json.dumps(sparkJsonSafe(alert)), mimetype='application/json'), 201


@app.route('/rooms', methods=['GET'])
def get_rooms():
    return Response(json.dumps(sparkJsonSafe(spark.getRooms())), mimetype='application/json')


@app.route('/rooms', methods=['POST'])
def create_room():
    room = request.json
    return Response(json.dumps(sparkJsonSafe(spark.createRoom(room['title']))), mimetype='application/json'), 201


@app.route('/rooms/<string:title>', methods=['GET'])
def get_room(title):
    room = spark.getRoom(title)
    if not room:
        return ('', 404)
    return Response(json.dumps(sparkJsonSafe(room)), mimetype='application/json')


@app.route('/rooms/<string:title>', methods=['DELETE'])
def delete_room(title):
    spark.deleteRoom(title)
    return ('', 204)


@app.route('/rooms/<string:title>/messages', methods=['GET'])
def get_room_messages(title):
    return Response(json.dumps(sparkJsonSafe(spark.getRoomMessages(title))), mimetype='application/json')


@app.route('/rooms/<string:title>/members', methods=['GET'])
def get_room_members(title):
    return Response(json.dumps(sparkJsonSafe(spark.getRoomMembers(title))), mimetype='application/json')


@app.route('/rooms/<string:title>/members', methods=['POST'])
def create_member(title):
    member = request.json
    return Response(json.dumps(sparkJsonSafe(spark.createRoomMembers(title, member['personEmail']))), mimetype='application/json'), 201


@app.route('/rooms/<string:title>/members/<string:email>', methods=['GET'])
def get_member(title, email):
    members = spark.getRoomMember(title, email)
    if not members:
        return ('', 404)
    return Response(json.dumps(sparkJsonSafe(members)), mimetype='application/json')


@app.route('/rooms/<string:title>/members/<string:email>', methods=['DELETE'])
def delete_member(title, email):
    spark.deleteRoomMember(title, email)
    return ('', 204)


@app.route('/people/<string:email>', methods=['GET'])
def get_person(email):
    person = spark.getPersonByEmail(email)
    if not person:
        return ('', 404)
    return Response(json.dumps(sparkJsonSafe(person)), mimetype='application/json')


@app.route('/webhooks', methods=['GET'])
def get_webhooks():
    return Response(json.dumps(sparkJsonSafe(spark.getWebhooks())), mimetype='application/json')


@app.route('/webhooks', methods=['POST'])
def create_webhook():
    webhook = request.json
    return Response(json.dumps(sparkJsonSafe(spark.createRoomWebhook(webhook['roomname'], webhook['url'], webhook['name']))), mimetype='application/json'), 201


@app.route('/webhooks/<string:webhookName>', methods=['GET'])
def get_webhook(webhookName):
    webhook = spark.getWebhook(webhookName)
    if not webhook:
        return ('', 404)
    return Response(json.dumps(sparkJsonSafe(webhook)), mimetype='application/json')


@app.route('/webhooks/<string:webhookName>', methods=['DELETE'])
def delete_webhook(webhookName):
    spark.deleteWebhook(webhookName)
    return ('', 204)


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
