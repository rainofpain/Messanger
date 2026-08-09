import flask
import flask_login
from Project.db import DATABASE
from .models import Chat, user_chats, Message

def render_chat():
    user = flask_login.current_user._get_current_object()

    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/authorization")
    
    user_chat = Chat.query.filter_by(owner_id = user.id).first()
    chats = Chat.query.all()
    chats = [{"id": chat.id, "name": chat.name} for chat in chats]
    
    if flask.request.method == "POST":
        data = flask.request.get_json()
        
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
                
            return flask.render_template("chat.html", user_chat = chat, chats = chats, user = user)

        if data.get("action") == "enter-chat":
            user_chat = DATABASE.session.query(user_chats).filter_by(
                chat_id= int(data.get("chatId")), 
                user_id = user.id
            )

            is_member = DATABASE.session.query(user_chat.exists()).scalar()
            return flask.jsonify({"is_member": is_member}), 200
        
        if data.get("action") == "add-user-to-chat":
            entrance_chat_id = data.get("chatId")
            entrance_chat = Chat.query.get(entrance_chat_id)
            if not entrance_chat:
                return ""

            entrance_chat.members.append(user)
            DATABASE.session.commit()
            return ""

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

    
    return flask.render_template("chat.html", user_chat = user_chat, chats = chats, user = user)
    
    
def render_chat_room(chat_id):

    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/authorization")
    
    user = flask_login.current_user._get_current_object()
    user_chat = DATABASE.session.query(user_chats).filter_by(
            chat_id= chat_id, 
            user_id = user.id
        )
    is_member = DATABASE.session.query(user_chat.exists()).scalar()

    if not is_member:
        return flask.redirect("/chat")
    
    current_chat = Chat.query.get(chat_id)

    user_chat = Chat.query.filter_by(owner_id = user.id).first()
    chats = Chat.query.all()
    chats = [{"id": chat.id, "name": chat.name} for chat in chats]
    
    if flask.request.method == "POST":
        data = flask.request.get_json()

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
                
            return flask.render_template(
                "chat.html", 
                user_chat = chat, 
                chats = chats, 
                user = user,
                messages = current_chat.messages
                )
        
        if data.get("action") == "send_message":
            message_text = data.get("message")
            if not message_text:
                return ""

            message_to_save = Message(
                chat_id = chat_id,
                sender_id = user.id,
                text = message_text
            )
            DATABASE.session.add(message_to_save)
            DATABASE.session.commit()

            return ""

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

    
    return flask.render_template("chat.html", user_chat = user_chat, chats = chats, user = user, messages = current_chat.messages)