import traceback
import simplejson as json
import logging
from flask import Flask, request, Response
from flask.ext.cors import CORS
from libs.restException import RestException
from flask_socketio import SocketIO, emit
from libs.tropoService import TropoService

app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app)
actions = []
tropo = TropoService(logging)


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


# base route for getting the lighting system data
@app.route('/actions', methods=['GET'])
def get_actions():
    return Response(json.dumps(actions), mimetype='application/json')


# route to create a light system
@app.route('/actions', methods=['POST'])
def create_light_system():
    action = request.json
    if action['type'] == tropo:
        tropo.sendMessages(action.message, action.phoneNumbers)
    actions.append(action)
    return Response(json.dumps(action), mimetype='application/json'), 201


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
