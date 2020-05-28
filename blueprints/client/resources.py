from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Client
from blueprints import db, app, internal_required
from sqlalchemy import desc
import uuid
import hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

# using flask restful


class ClientResource(Resource):

    def get(self, id=None):
        qry = Client.query.get(id)
        if qry is not None:
            return marshal(qry, Client.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('internal', type=bool,
                            location='json', required=False)
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        hash_pass = hashlib.sha512(
            ('%s%s' % (args['password'], salt)).encode('utf-8')).hexdigest()

        client = Client(args['username'], hash_pass, salt, args['internal'])
        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)
        return marshal(client, Client.response_fields), 200, {'Content-Type': 'application/json'}


    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        data = parser.parse_args()

        qry = Client.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (data['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        qry.username = data['username']
        qry.password = hash_pass
        qry.salt = salt
        db.session.commit()
        return marshal(qry, Client.response_fields), 200


    def delete(self, id):
        qry = Client.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()


    def patch(self):
        return 'Not yet implement', 501

    def options(self):
        return {}, 200


class ClientList(Resource):
    def __init__(self):
        pass


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('username', location='args',
                            help='invalid status')
        parser.add_argument('orderby', location='args',
                            help='invalid order by value')
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = Client.query
        if args['username'] is not None:
            qry = qry.filter_by(username=args['username'])

        if args['orderby'] is not None:
            if args['orderby'] == 'username':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Client.username))
                else:
                    qry = qry.order_by(Client.username)
            elif args['orderby'] == 'password':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Client.password))
                else:
                    qry = qry.order_by(Client.password)
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Client.response_fields))
        return rows, 200


api.add_resource(ClientList, '', '/list')
api.add_resource(ClientResource, '', '/<id>')
