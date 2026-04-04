from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import TipoMovimientoCategoria


class VistaCategorias(Resource):

    @jwt_required()
    def get(self):
        return jsonify([tipo_categoria.name for tipo_categoria in TipoMovimientoCategoria])