import flask 
import os
from flask_mailman import Mail

project = flask.Flask(
    import_name = "Project",
    static_url_path = "/static",
    template_folder = "templates",
    static_folder = "static",
    instance_path = os.path.abspath(os.path.join(__file__, "..", "instance"))
)

MAIL_SENDER = os.getenv("MAIL_SENDER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

project.config['MAIL_SERVER'] = 'smtp.gmail.com'
project.config['MAIL_PORT'] = 587
project.config['MAIL_USE_TLS'] = True
project.config['MAIL_USERNAME'] = MAIL_SENDER
project.config['MAIL_PASSWORD'] = MAIL_PASSWORD
project.config['MAIL_DEFAULT_SENDER'] = MAIL_SENDER

mail = Mail(app = project)