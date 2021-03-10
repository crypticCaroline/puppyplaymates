import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_socketIO import SocketIO, send, emit

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

socketio = SocketIO(app)
mongo = PyMongo(app)

@app.route("/")
@app.route('/woofchat', methods=["GET", "POST"])
def woof_chat():
    return render_template('woof_chat.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('message')
def handle_message(message):
    send(message, namespace='/chat')


@socketio.on('my event')
def handle_my_custom_event(username, methods=['GET', 'POST']):
    emit('my response', username=username, namespace='/chat')


@socketio.on("event")
def my_event(message):
    print('my response', {'data': 'got it!'})


if __name__ == "__main__":
    socketio.run(app,
                 host=os.environ.get("IP"),
                 port=int(os.environ.get("PORT")),
                 debug=True)


# @app.errorhandler(werkzeug.exceptions.BadRequest)
# def handle_bad_request(e):
#     return 'bad request!', 400