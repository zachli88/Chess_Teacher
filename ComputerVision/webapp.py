from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='./templates')
socketio = SocketIO(app)

transmit_data = "NA"

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect(conn):
    print('connected')
    print(conn)
    socketio.emit('message',data=transmit_data)

@socketio.on('message')
def handle_data(message):
    global transmit_data
    if(message != transmit_data):
        print(f"emitting {transmit_data}")
    socketio.emit('message', data=transmit_data)

def update_data(data):
    global transmit_data
    transmit_data = data
    print("updated data...")

def start():
    socketio.run(app, port=5050)
    print("hey")

if __name__ == "__main__":
    start()