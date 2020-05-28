from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints.client.model import Client
from blueprints.user.model import User
from blueprints import db, app, internal_required
from sqlalchemy import desc
import uuid
import hashlib

bp_register = Blueprint('register', __name__)
api = Api(bp_register)


class RegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('internal', type=bool,
                            location='json')
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json',
                            required=True, choices=('male', 'female'))
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('telephone', location='json', required=True)
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        hash_pass = hashlib.sha512(
            ('%s%s' % (args['password'], salt)).encode('utf-8')).hexdigest()

        client = Client(args['username'], hash_pass, salt, args['internal'])
        db.session.add(client)
        db.session.flush()
        user = User(client.client_id, args['name'],
                    args['age'], args['sex'], args['address'], args['email'], args['telephone'])

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)
        app.logger.debug('DEBUG : %s', user)
        row = [marshal(client, Client.response_fields),
               marshal(user, User.response_fields)]
        return row, 200


api.add_resource(RegisterResource, '', '/<id>')
