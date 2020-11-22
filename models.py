from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db=SQLAlchemy()
bcrypt=Bcrypt()

def connect_db(app):
    db.app=app
    db.init_app(app)

class User(db.Model):
    """ User Table"""
    __tablename__='users'

    username=db.Column(db.String(20),
                primary_key=True, unique=True, nullable=False)
    password=db.Column(db.Text, nullable=False)
    email=db.Column(db.String(50),unique=True,nullable=False)
    first_name=db.Column(db.String(30),nullable=False)
    last_name=db.Column(db.String(30),nullable=False)
    feedbacks=db.relationship('Feedback', backref='user', cascade='all,delete-orphan')


    @classmethod
    def register(cls,username,pwd):
        """Registiration class method"""
        hashed=bcrypt.generate_password_hash(pwd)
        hashed_utf8=hashed.decode('utf8')
        return hashed_utf8

    @classmethod
    def authenticate(cls,username,pwd):
        """Authentication class method"""
        u=User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False

class Feedback(db.Model):
    """ Feedback Table"""
    __tablename__='feedbacks'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    username=db.Column(db.String(20), db.ForeignKey('users.username'))
    