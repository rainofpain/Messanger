import flask
import flask_login
from Project.db import DATABASE
from .models import Chat

def render_chat():
    user = flask_login.current_user

    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/authorization")
    
    user_chat = Chat.query.filter_by(owner_id = user.id).first()
    chats = Chat.query.all()
    chats = [{"id": chat.id, "name": chat.name} for chat in chats]
    
    if flask.request.method == "POST":

        if "send-user-data" in flask.request.form:
            first_name = flask.request.form["first_name"]
            surname = flask.request.form["surname"]
            username = flask.request.form["username"]
            gender = flask.request.form.get('gender')


            if first_name and surname and username and gender:
                user.first_name = first_name
                user.surname = surname
                user.username = username
                user.gender = gender
                DATABASE.session.commit()
            
            return flask.render_template("chat.html")
        if "create-chat" in flask.request.form and not user_chat:
            chat_name = flask.request.form["chat_name"].strip()
            if chat_name and chat_name != "":
                chat = Chat(
                    name = chat_name,
                    owner_id = user.id
                    )
                chat.owner = user
                chat.members.append(user)
                DATABASE.session.commit()

                chats = Chat.query.all()
                chats = [{"id": chat.id, "name": chat.name} for chat in chats]
                
            return flask.render_template("chat.html", user_chat = chat, chats = chats)

    if flask.request.method == "DELETE":
        data = flask.request.get_json()

        if data.get("action") == "delete-account":
            user_to_delete = flask_login.current_user._get_current_object()
            flask_login.logout_user()
            DATABASE.session.delete(user_to_delete)
            DATABASE.session.commit()
            return ''
        
        if data.get("action") == "delete-chat":

            chat_to_delete = Chat.query.filter_by(owner_id = user.id).first()
            DATABASE.session.delete(chat_to_delete)
            DATABASE.session.commit()
            return ''

    
    return flask.render_template("chat.html", user_chat = user_chat, chats = chats)
    
    
    