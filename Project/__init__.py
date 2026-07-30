from .urls import *
from .settings import project, MAIL_SENDER, socket_app
from .db import *
from .loadenv import execute
from .login_manager import *

from user.models import User
from chat.models import *

project.register_blueprint(blueprint= user.user)
project.register_blueprint(blueprint= chat.chat)