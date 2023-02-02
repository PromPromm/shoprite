from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import StoreModel
from schemas import StoreSchema, PlainStoreSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("store", __name__, description='Operations on stores')

@blp.route("/store")
class StoreList(MethodView):
    #@StoreBlueprint.response(200, StoreSchema(many=True))
    @jwt_required()
    @blp.response(200, PlainStoreSchema(many=True))
    def get(self):
        stores = StoreModel.query.all()
        return stores

    @jwt_required()
    @blp.arguments(PlainStoreSchema)
    @blp.response(200, PlainStoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while creating the store')
        return store, 201


@blp.route("/store/<store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {"message": "Store deleted"}
