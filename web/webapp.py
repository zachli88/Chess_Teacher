from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
from queue import Queue
import json
from threading import Thread


app = Flask(__name__, template_folder='./templates')
socketio = SocketIO(app, async_mode='threading')

outgoing_queue = Queue()
incoming_queue = Queue()

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def connect():
    print('client connected...')
    transmitter = Thread(target=post_message, args=())
    transmitter.start()

@socketio.on('client_message')
def incoming(data):
    incoming_queue.put(data)
    print("recieved req from client")
    

def post_message():
    while True:
        message = outgoing_queue.get()
        socketio.emit('message', message)
        # print("emitted " + str(message))


def push_message(prefix, message, data=None):
    outgoing_queue.put(json.dumps([prefix, message, data]))
    print(f"pushed {str(prefix)} to queue")


def await_message():
    msg = incoming_queue.get()
    return msg


def start():
    socketio.run(app, port=4090, )
    print("starting server...")


if __name__ == "__main__":
    start()