from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import User
from blueprints import db, app, internal_required
from sqlalchemy import desc
from blueprints.post.model import Post
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

# using flask restful


class UserResource(Resource):

    # @internal_required
    def get(self, id=None):
        qry = User.query.get(id)
        if qry is not None:
            QRY = marshal(qry, User.response_fields)
            post = Post.query.filter_by(
                seller_id=QRY['id']).first()
            QRY['POST'] = marshal(post, Post.response_fields)
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404

    # @internal_required
    def post(self):
        claims = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json',
                            required=True, choices=('male', 'female'))
        parser.add_argument('address', location='json', required=True)
        parser.add_argument('email', location='json', required=True)
        parser.add_argument('telephone', location='json', required=True)

        args = parser.parse_args()
        user = User(args['name'],
                    args['age'], args['sex'], args['address'], args['email'], args['telephone'], claims['client_id'])

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)
        return marshal(user, User.response_fields), 200, {'Content-Type': 'application/json'}

    # @internal_required
    def patch(self, id):
        claims = get_jwt_claims()
        qry = User.query.filter_by(client_id=claims['client_id']).first()
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        else:
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='json', required=True)
            parser.add_argument('age', location='json',
                                type=int, required=True)
            parser.add_argument('sex', location='json',
                                required=True, choices=('male', 'female'))
            parser.add_argument('address', location='json', required=True)
            parser.add_argument('email', location='json', required=True)
            parser.add_argument('telephone', location='json', required=True)

            args = parser.parse_args()

            qry.name = args['name']
            qry.age = args['age']
            qry.sex = args['sex']
            qry.address = args['address']
            qry.email = args['email']
            qry.telephone = args['telephone']
            db.session.commit()

            return marshal(qry, User.response_fields), 200

    # @internal_required
    def delete(self, id):
        qry = User.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200


class UserList(Resource):
    def __init__(self):
        pass

    # @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('sex', location='args',
                            help='invalid status', choices=('male', 'female'))
        parser.add_argument('orderby', location='args',
                            help='invalid order by value', choices=('age', 'sex'))
        parser.add_argument('sort', location='args',
                            help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()
        offset = (args['p'] * args['rp']) - args['rp']
        qry = User.query
        if args['sex'] is not None:
            qry = qry.filter_by(sex=args['sex'])

        if args['orderby'] is not None:
            if args['orderby'] == 'age':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(User.age))
                else:
                    qry = qry.order_by(User.age)
            elif args['orderby'] == 'sex':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(User.sex))
                else:
                    qry = qry.order_by(User.sex)
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, User.response_fields))
        return rows, 200


api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, '', '/<id>')
