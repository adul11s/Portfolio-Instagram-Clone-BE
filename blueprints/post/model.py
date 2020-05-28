from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from blueprints.user.model import User
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(30), unique=True, nullable=False)
    image = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'description': fields.String,
        'image': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
    }

    def __init__(self, user_id, description, image):
        
        self.user_id = seller_id
        self.description = description
        self.image = image

    def __repr__(self):
        return '<Post %r>' % self.id
