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
    # print('client connected...')
    transmitter = Thread(target=post_message, args=())
    transmitter.start()

last_data = None

@socketio.on('client_message')
def incoming(data):
    global last_data

    if data == last_data:
        return
    
    print("recieved req from client")
    print("req info: " + data)
    incoming_queue.put(data)
    last_data = data
    
    
counter = 0

def post_message():
    global outgoing_queue
    global counter
    # while True:
    message = outgoing_queue.get()
        # message = counter
        # print("sending message")
        # print("message changed")
        # while outgoing_queue.empty():
            # print("resending..." + str(message))
    socketio.emit('message', message)
        # counter += 1


def push_message(prefix, message, data=None):
    global outgoing_queue
    outgoing_queue.put(json.dumps([prefix, message, data]))
    print(f"pushed {str(prefix)} to queue")


def await_message():
    global incoming_queue
    msg = incoming_queue.get()
    return msg


def start():
    socketio.run(app, port=4090, )
    print("starting server...")


if __name__ == "__main__":
    start()