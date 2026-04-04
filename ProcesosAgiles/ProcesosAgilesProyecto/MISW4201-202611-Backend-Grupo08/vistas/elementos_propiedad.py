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

class VistaElementosPropiedad(Resource):

    @jwt_required()
    def post(self, id_propiedad): 
        
        try:
            # Verificar que la propiedad pertenezca al usuario actual o sea su administrador
            propiedad = Propiedad.query.filter(
                Propiedad.id == id_propiedad,
                (Propiedad.id_usuario == current_user.id) | (Propiedad.id_admin == current_user.id)
            ).first()

            # En caso de no presentar resultados, se arroja un mensaje de error
            if not propiedad:
                return {"mensaje": "Propiedad no encontrada o no autorizada"}, 404

            # Cargar datos del elemento
            nuevo_elemento = elemento_propiedad_schema.load(request.json, session = db.session)
            
            # Asignar la relación automática (Criterio de la HU)
            nuevo_elemento.id_propiedad = id_propiedad
            
            # Agregamos el nuevo elemento
            db.session.add(nuevo_elemento)
            
            # Aplicamos cambios
            db.session.commit()

            # Retorno de mensaje de éxito
            return elemento_propiedad_schema.dump(nuevo_elemento), 201

        # Retorno de mensaje inválido
        except ValidationError as err:
            print("--- ERROR DE VALIDACIÓN MARSHMALLOW ---")
            print(err.messages) # <--- ESTO APARECERÁ EN TU TERMINAL DE UBUNTU
            print("---------------------------------------")
            
            return err.messages, 400
        
        # En caso de una excepción
        except Exception:

            # Revertir cambios
            db.session.rollback()

            # Retorno de mensaje de error
            return {"mensaje": "Error al crear el elemento"}, 500
    
    @jwt_required()
    def get(self, id_propiedad):

        # Filtramos por la primera propiedad
        propiedad = Propiedad.query.filter(
            Propiedad.id == id_propiedad,
            (Propiedad.id_usuario == current_user.id) | (Propiedad.id_admin == current_user.id)
        ).first()
        
        # Se retorna un error en caso de que no arroje resultados
        if not propiedad:
            return {"mensaje": "No autorizado"}, 401
        
        # Filtramos por los elementos de la propiedad
        elementos = ElementoPropiedad.query.filter_by(id_propiedad = id_propiedad).all()

        # Retorno de elementos de la propiedad
        return elemento_propiedad_schema.dump(elementos, many = True), 200