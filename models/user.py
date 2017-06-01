import sqlite3
from db import db

# Model = our internal representation of an entity.
# Resource = external representation of an entity.
#            It is used to map end points, such as the get
#            verb, the post verb and delete put verbs.

# API clients = website or a mobile app interact with resources.
# REST APIs => respond by resources.

# Models and Resources are linked, by clearly separeted.

# This class is NOT a resource, because the API cannot
# receive data into this class or send this class as a
# JSON representation. So this class here is a helper.  
class UserModel(db.Model): # Extends db model

    # Telling SQLAlchemy about our tables and columns
    __tablename__ = 'users'

    # N.B.: primary_key=True => auto increment, automatically generated by db engine
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod # use the current class User
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first() # SELECT * FROM users

    @classmethod # use the current class User
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()