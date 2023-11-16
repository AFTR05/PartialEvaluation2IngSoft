from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, data):
        for observer in self._observers:
            observer.update(data)

class EmailSystem(Observable):
    def __init__(self):
        super().__init__()
        self.inbox = {}

    def send_email(self, sender, recipient, subject, body):
        if recipient not in self.inbox:
            self.inbox[recipient] = []

        email = {
            'sender': sender,
            'subject': subject,
            'body': body
        }

        self.inbox[recipient].append(email)
        self.notify_observers(email)

    def get_inbox(self, username):
        return self.inbox.get(username, [])

class UIUpdater:
    def __init__(self, socketio, username):
        self.socketio = socketio
        self.username = username

    def update(self, data):
        self.socketio.emit('receive_email', {'username': self.username, 'email': data})

def periodic_update(email_system, username):
    while True:
        inbox = email_system.get_inbox(username)
        socketio.emit('inbox_update', {'username': username, 'inbox': inbox})
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_email')
def handle_send_email(data):
    email_system.send_email(data['sender'], data['recipient'], data['subject'], data['body'])

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    email_system = EmailSystem()

    ui_updater = UIUpdater(socketio, "destinatario")
    email_system.add_observer(ui_updater)



    socketio.run(app, debug=True)
