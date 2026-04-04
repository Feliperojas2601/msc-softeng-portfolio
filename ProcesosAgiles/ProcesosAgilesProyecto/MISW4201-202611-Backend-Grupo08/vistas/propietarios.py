from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import Usuario


class VistaPropietarios(Resource):

    @jwt_required()
    def get(self):
        propietarios = Usuario.query.filter_by(rol=Usuario.ROL_PROPIETARIO).all()
        return [{'id': p.id, 'usuario': p.usuario} for p in propietarios], 200
