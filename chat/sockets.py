import socket
from flask_socketio import join_room, leave_room, emit
import flask

from Project.settings import socket_app


@socket_app.on("connect")
def handle_send_message():
    
    print("Connected", flask.request.sid)

@socket_app.on("join")
def on_join(data: dict):
    chat = data.get("chat")
    join_room(chat)  
    print(f"User {flask.request.sid} приєднався до чату: {chat}")


@socket_app.on("send_to_room")
def handle_message_room(data: dict):
    chat = data.get("chat")
    message = data.get("message")
    
    emit("new_message", {"message": message}, to = chat)

@socket_app.on("leave")
def on_leave(data: dict):
    chat = data.get("chat")
    leave_room(chat)
    emit("status", {"msg": "Користувач покинув чат"}, to = chat)