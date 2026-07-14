import flask
import flask_login
import os

from itsdangerous import URLSafeTimedSerializer
from flask_mailman.message import EmailMultiAlternatives
from email.mime.image import MIMEImage

from Project.db import DATABASE
from Project.settings import MAIL_SENDER




from .models import User


def render_registration() -> dict:
    if flask.request.method == "POST":
        password = flask.request.form["password"]
        confirm_password = flask.request.form["confirm_password"]
        email_form = flask.request.form["email"]

        email_model = User.query.filter_by(email = email_form).scalar()
        
        if email_model is None:
            if password == confirm_password:
                user = User(
                    email = email_form,
                    password = password
                )
                DATABASE.session.add(user)
                DATABASE.session.commit()
                user_email = flask.request.form.get('email')
        
                serializer = URLSafeTimedSerializer("SECRET_KEY_FOR_SALT")
                token = serializer.dumps(user_email, salt="email-confirm-salt")

                confirm_url = flask.url_for('user.confirm_email', token=token, _external=True)
                
                msg = EmailMultiAlternatives(
                    subject="Перевірка пошти",
                    body="",
                    from_email= MAIL_SENDER,
                    to=[user_email]
                    )
                
                html_content = flask.render_template("email_message.html", confirm_url = confirm_url)
            
                image_path = os.path.join(__file__, '..', '..', 'Project', 'static', 'images', 'email_img.png')

                with open(image_path, 'rb') as fp:
                    msg_image = MIMEImage(fp.read())
    
                    msg_image.add_header('Content-ID', '<my_image_cid>')
                    
                    msg_image.add_header('Content-Disposition', 'inline', filename='email_img.png')
                    
                    msg.attach(msg_image)

                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return flask.redirect("/redirect_to_email")    
                  
    return flask.render_template("registration.html")
    
def render_redirect_to_email():
    return flask.render_template("email_redirect.html")

def render_authorization():
    
    if flask.request.method == "POST":
        email_form = flask.request.form["email"]
        password_form = flask.request.form["password"]

        list_users = User.query.all()
        for user in list_users:
            if user.email == email_form and user.password == password_form and user.confirmed_email != 0:
                flask_login.login_user(user)
    if not flask_login.current_user.is_authenticated:
        return flask.render_template("authorization.html")
    else:
        return flask.redirect("/")
    

def confirm_email(token):
    serializer = URLSafeTimedSerializer("SECRET_KEY_FOR_SALT")
    try:
       
        email = serializer.loads(token, salt="email-confirm-salt")
        user = User.query.filter_by(email=email).first()
        user.confirmed_email = True
        DATABASE.session.commit()
    except:
        return "Посилання недійсне або його термін дії закінчився!", 400
        
    return flask.redirect("/authorization")

def logout():
    flask.session.clear()
    return flask.redirect("/authorization")    