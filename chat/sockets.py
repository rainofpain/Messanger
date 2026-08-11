import socket
from flask_socketio import join_room, leave_room, emit
import flask
import flask_login

from Project.settings import socket_app

online_users = set()

@socket_app.on("connect")
def handle_connect():
    current_user = flask_login.current_user
    if current_user.is_authenticated:
        if current_user.id not in online_users:
            online_users.add(current_user.id)
            emit("user_status_change", {"user_id": current_user.id, "status": "online"}, broadcast=True)
        join_room(f"user_{current_user.id}")


@socket_app.on("disconnect")
def handle_disconnect():
    current_user = flask_login.current_user
    if current_user.is_authenticated:
        leave_room(f"user_{current_user.id}")
        room_sids = socket_app.server.manager.rooms.get("/", {}).get(f"user_{current_user.id}")

        if not room_sids:
            online_users.discard(current_user.id)
            emit("user_status_change", {"user_id": current_user.id, "status": "offline"}, broadcast=True)

@socket_app.on("join")
def on_join(data: dict):
    chat = data.get("chat")
    join_room(chat)  
    print(f"User {flask.request.sid} приєднався до чату: {chat}")


@socket_app.on("send_to_chat")
def handle_message_room(data: dict):
    user = flask_login.current_user._get_current_object()
    user_email = user.email
    chat = data.get("chat")
    message = data.get("message")

    
    emit("new_message", {"message": message, "user_email": user_email}, to = chat)

@socket_app.on("leave")
def on_leave(data: dict):
    chat = data.get("chat")
    leave_room(chat)
    emit("status", {"msg": "Користувач покинув чат"}, to = chat)