from Project.db import DATABASE
from flask_login import UserMixin

class User(DATABASE.Model, UserMixin):
    
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    
    first_name = DATABASE.Column(DATABASE.String(50),default = "", nullable = True)
    surname = DATABASE.Column(DATABASE.String(50),default = "", nullable = True)
    username = DATABASE.Column(DATABASE.String(50),default = "anonymous", nullable = True)
    gender = DATABASE.Column(DATABASE.String(50), nullable = True)
    email = DATABASE.Column(DATABASE.String(50), nullable = False)
    password = DATABASE.Column(DATABASE.String(25), nullable = False)

    confirmed_email = DATABASE.Column(DATABASE.Boolean, default = False, nullable = False)
    is_admin = DATABASE.Column(DATABASE.Boolean, default = False)