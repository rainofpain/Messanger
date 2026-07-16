import flask
import flask_login
from Project.db import DATABASE

def render_chat():
    user = flask_login.current_user
    if not flask_login.current_user.is_authenticated:
        return flask.redirect("/authorization")
    if flask.request.method == "POST":

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

    if flask.request.method == "DELETE":
        user_to_delete = flask_login.current_user._get_current_object()
        flask_login.logout_user()
        DATABASE.session.delete(user_to_delete)
        DATABASE.session.commit()
        return ''
    
    return flask.render_template("chat.html")