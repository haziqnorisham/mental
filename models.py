import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import func

db = SQLAlchemy()



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    message = db.Column(db.Text, unique=False, nullable=False)

    def __repr__(self):
        return '<Message %r>' % self.id
