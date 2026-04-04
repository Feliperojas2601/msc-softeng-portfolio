from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import PeriodicidadMantenimiento


class VistaPeriodicidadMantenimientos(Resource):

    @jwt_required()
    def get(self):
        return jsonify([p.value for p in PeriodicidadMantenimiento])
