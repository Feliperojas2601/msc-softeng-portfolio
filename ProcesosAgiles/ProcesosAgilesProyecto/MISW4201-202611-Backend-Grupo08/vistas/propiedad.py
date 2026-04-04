from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource
from sqlalchemy import delete, select
from modelos import Propiedad, PropiedadSchema, db
from vistas.utils import buscar_propiedad

propiedad_schema = PropiedadSchema()

class VistaPropiedad(Resource):

    @jwt_required()
    def put(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        for key, value in request.json.items():
            setattr(resultado_buscar_propiedad.entidad, key, value)
        db.session.commit()
        return propiedad_schema.dump(resultado_buscar_propiedad.entidad)
    
    @jwt_required()
    def delete(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        db.session.execute(delete(Propiedad).filter(Propiedad.id == id_propiedad))
        db.session.commit()
        return "", 204
    
    @jwt_required()
    def get(self, id_propiedad):
        resultado_buscar_propiedad = buscar_propiedad(id_propiedad, current_user.id)
        if resultado_buscar_propiedad.error:
            return resultado_buscar_propiedad.error
        return propiedad_schema.dump(resultado_buscar_propiedad.entidad)

    def patch(self, id_propiedad):
        propiedad = db.session.execute(
            select(Propiedad).filter(Propiedad.id == id_propiedad)
        ).scalar_one_or_none()
        if not propiedad:
            return {'mensaje': 'propiedad no encontrada'}, 404
        id_admin = request.json.get('id_admin')
        if id_admin is None:
            return {'mensaje': 'id_admin es requerido'}, 400
        propiedad.id_admin = id_admin
        db.session.commit()
        return propiedad_schema.dump(propiedad)
