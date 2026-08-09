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
    messages = DATABASE.relationship('Message', back_populates='chat', cascade="all, delete-orphan")

class Message(DATABASE.Model):
    __tablename__ = 'messages'

    id = DATABASE.Column(DATABASE.Integer, primary_key=True)
    text = DATABASE.Column(DATABASE.Text, nullable=False)
    
    chat_id = DATABASE.Column(
        DATABASE.Integer, 
        DATABASE.ForeignKey('chats.id', ondelete="CASCADE"), 
        nullable=False
    )
    chat = DATABASE.relationship('Chat', back_populates='messages')

    sender_id = DATABASE.Column(
    DATABASE.Integer,
    DATABASE.ForeignKey('users.id', ondelete="SET NULL"),
    nullable=True 
    )
    user = DATABASE.relationship('User', back_populates='messages') 