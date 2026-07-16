from .urls import *
from .settings import project, MAIL_SENDER
from .db import *
from .loadenv import execute
from .login_manager import *

from user.models import User

project.register_blueprint(blueprint= user.user)
project.register_blueprint(blueprint= chat.chat)