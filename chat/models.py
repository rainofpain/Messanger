from Project.db import DATABASE

user_chats = DATABASE.Table('user_chats',
    DATABASE.Column('user_id', DATABASE.Integer, DATABASE.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    DATABASE.Column('chat_id', DATABASE.Integer, DATABASE.ForeignKey('chats.id', ondelete="CASCADE"), primary_key=True)
)

class Chat(DATABASE.Model):
    __tablename__ = 'chats'
    
    id = DATABASE.Column(DATABASE.Integer, primary_key = True)
    name = DATABASE.Column(DATABASE.String(50),unique = True, nullable = False)
    owner_id = DATABASE.Column(
        DATABASE.Integer, 
        DATABASE.ForeignKey('users.id'),
        unique=True,                     
        nullable=False                   
    )

    owner = DATABASE.relationship('User', backref='owner', uselist=False)
    members = DATABASE.relationship('User', secondary = user_chats, backref = 'chats')