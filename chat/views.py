import flask
import flask_login
from Project.db import DATABASE
from .models import Chat, user_chats, Message
from user.models import User
from .sockets import online_users 

def render_chat():
    user = flask_login.current_user._get_current_object()

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
            
            return flask.render_template(
                    "chat.html", 
                    user_chat = user_chat, 
                    chats = chats, 
                    user = user
                )
        
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
                    user = user
                )

        data = flask.request.get_json()

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

    
    return flask.render_template(
            "chat.html", 
            user_chat = user_chat, 
            chats = chats, 
            user = user
        )
    
    
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
            
            return flask.render_template(
                    "chat_open.html", 
                    user_chat = user_chat, 
                    chats = chats, 
                    user = user, 
                    current_chat = current_chat,
                    online_users = online_users
                )
        
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
                    "chat_open.html", 
                    user_chat = chat, 
                    chats = chats, 
                    user = user,
                    current_chat = current_chat,
                    online_users = online_users
                )
        
        data = flask.request.get_json()

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
        
        if data.get("action") == "click_on_member":
            member_id = data.get("memberId")
            if not member_id:
                return print("no id")

            member = User.query.get(member_id)

            if not member:
                return print("no member")

            member_name = member.first_name
            member_surname = member.surname
            member_username = member.username
            member_gender = member.gender

            return flask.jsonify(
                    {
                        "member_name": member_name,
                        "member_surname": member_surname,
                        "member_username": member_username,
                        "member_gender": member_gender
                    }
                ), 200


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

    
    return flask.render_template(
            "chat_open.html",
            user_chat = user_chat, 
            chats = chats, user = user,
            current_chat = current_chat,
            online_users = online_users
        )