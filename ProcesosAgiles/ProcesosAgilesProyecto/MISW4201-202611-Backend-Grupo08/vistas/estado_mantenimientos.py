from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import EstadoMantenimiento


class VistaEstadoMantenimientos(Resource):

    @jwt_required()
    def get(self):
        return jsonify([estado_mantenimiento.name for estado_mantenimiento in EstadoMantenimiento])