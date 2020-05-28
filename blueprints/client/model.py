from blueprints import db
from flask_restful import fields
from sqlalchemy.orm import relationship


class Client(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, default=20)
    salt = db.Column(db.String(255))
    internal = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship('User', backref='client', lazy=True)

    response_fields = {
        'client_id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'internal': fields.Boolean
    }
    jwt_claim_fields = {
        'client_id': fields.Integer,
        'username': fields.String,
        'internal': fields.Boolean
    }

    def __init__(self, username, password, salt, internal):
        self.username = username
        self.password = password
        self.salt = salt
        self.internal = internal

    def __repr__(self):
        return '<Client %r>' % self.client_id
