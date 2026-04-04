# 3rd Party Libraries
from flask import request
from sqlalchemy import exc, select
from flask_restful import Resource
from marshmallow import ValidationError
from vistas.utils import buscar_propiedad
from flask_jwt_extended import current_user, jwt_required
from modelos import ElementoPropiedad, Propiedad, db, ElementoPropiedadSchema

# Instanciar Elemento Propiedad Esquema
elemento_propiedad_schema = ElementoPropiedadSchema()

class VistaElementoPropiedad(Resource):
        
    @jwt_required()
    def put(self, id_propiedad, id_elemento):

        # Filtramos por la primera propiedad
        propiedad = Propiedad.query.filter(
            Propiedad.id == id_propiedad,
            (Propiedad.id_usuario == current_user.id) | (Propiedad.id_admin == current_user.id)
        ).first()
        
        # Se retorna un error en caso de que no arroje resultados
        if not propiedad:
            return {"mensaje": "No autorizado"}, 401
        
        # Filtramos por el elemento de la propiedad
        elemento = ElementoPropiedad.query.filter_by(id = id_elemento, id_propiedad = id_propiedad).first()

        # En caso de que el elemento no se encuentre
        if not elemento:
            return {"mensaje": "Elemento no encontrado en esta propiedad"}, 404
        
        try:

            # Cargar los cambios sobre la instancia existente
            elemento_actualizado = elemento_propiedad_schema.load(request.json, instance = elemento, session = db.session, partial = True)
            
            # Aseguramos que el id_propiedad no cambie por error en el JSON
            elemento_actualizado.id_propiedad = id_propiedad
            
            # 4. Guardar cambios
            db.session.commit()
            
            # 5. Retornar el objeto actualizado
            return elemento_propiedad_schema.dump(elemento_actualizado), 200

        # Si se produce algún error
        except ValidationError as err:
            return err.messages, 400
        
        # En caso de una excepción
        except Exception:
            db.session.rollback()
            return {"mensaje": "Error al actualizar el elemento"}, 500
    
    @jwt_required()
    def delete(self, id_propiedad, id_elemento):

        # Filtramos por la primera propiedad
        propiedad = Propiedad.query.filter(
            Propiedad.id == id_propiedad,
            (Propiedad.id_usuario == current_user.id) | (Propiedad.id_admin == current_user.id)
        ).first()
        
        # Se retorna un error en caso de que no arroje resultados
        if not propiedad:
            return {"mensaje": "No autorizado"}, 401
        
        # Filtramos por el elemento de la propiedad
        elemento = ElementoPropiedad.query.filter_by(id = id_elemento, id_propiedad = id_propiedad).first()

        # Conservar el nombre del elemento
        nombre = elemento.nombre

        # En caso de que el elemento no se encuentre
        if not elemento:
            return {"mensaje": "Elemento no encontrado en esta propiedad"}, 404

        # Eliminación del elemento y aplicación de cambios
        db.session.delete(elemento)
        db.session.commit()

        # Mensaje de retorno
        return {"mensaje": f"El elemento: {nombre}, ha sido eliminado exitosamente"}, 204
