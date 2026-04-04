from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import TipoCategoriaMantenimiento


class VistaTipoCategoriaMantenimientos(Resource):

    @jwt_required()
    def get(self):
        return jsonify([tipo_categoria_mantenimiento.name for tipo_categoria_mantenimiento in TipoCategoriaMantenimiento])
