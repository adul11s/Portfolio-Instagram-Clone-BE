from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from .model import Post
from blueprints import db, app, internal_required
from sqlalchemy import desc
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from blueprints.user.model import User

bp_post = Blueprint('post', __name__)
api = Api(bp_post)

# using flask restful


class PostResource(Resource):
    # @internal_required
    def get(self, id=None):
        qry = Post.query.get(id)
        if qry is not None:
            return marshal(qry, Post.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    # @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('description', location='json', required=True)
        parser.add_argument('image', location='json', required=True)
        args = parser.parse_args()
        claims = get_jwt_claims()
        qry = User.query.filter_by(id=claims["client_id"]).first()
      
        user_id = qry.id
        product = Product(user_id,
                          args['description'], args['image'])

        db.session.add(product)
        db.session.commit()

        app.logger.debug('DEBUG : %s', product)
        return marshal(product, Product.response_fields), 200, {'Content-Type': 'application/json'}

    # @jwt_required
    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('description', location='json', required=True)
        parser.add_argument('image', location='json', required=True)
        args = parser.parse_args()

        qry = Product.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
       
        qry.description = args['description']
        qry.image = args['image']

        db.session.commit()

        return marshal(qry, Product.response_fields), 200

    # @internal_required
    def delete(self, id):
        qry = Product.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        db.session.delete(qry)
        db.session.commit()

    def options(self):
        return {}, 200

