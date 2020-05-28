from blueprints import db
from flask_restful import fields
from sqlalchemy import Integer, ForeignKey, String, Column
from blueprints.client.model import Client
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, ForeignKey(Client.client_id))
    name = db.Column(db.String(30), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False, default=20)
    sex = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    telephone = db.Column(db.String(250), unique=True, nullable=False)
    post = db.relationship('Post', backref='user', lazy=True)
    follow = db.relationship('Follow', backref='user', lazy=True)

    response_fields = {
        'id': fields.Integer,
        'client_id': fields.Integer,
        'name': fields.String,
        'age': fields.Integer,
        'sex': fields.String,
        'address': fields.String,
        'email': fields.String,
        'telephone': fields.String
    }

    def __init__(self, client_id, name, age, sex, address, email, telephone):
        self.client_id = client_id
        self.name = name
        self.age = age
        self.sex = sex
        self.address = address
        self.email = email
        self.telephone = telephone

    def __repr__(self):
        return '<User %r>' % self.id
