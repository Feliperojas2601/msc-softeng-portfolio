# 1st Party Libraries
from modelos import Propiedad, db, Usuario, PropiedadSchema

# 3rd Party Libraries
from flask import request
from flask_restful import Resource
from sqlalchemy import exc, select
from marshmallow import ValidationError
from flask_jwt_extended import current_user, jwt_required

# Instanciar clase propiedad
propiedad_schema = PropiedadSchema()

class VistaPropiedades(Resource):
    """Clase que proporciona los métodos de creación y actualización de propiedades de corta estancia."""

    @jwt_required()
    def post(self): # Método 1
        
        # Confirmación del rol
        if current_user.rol != Usuario.ROL_PROPIETARIO:
            return {"mensaje": "Acceso denegado: Solo los propietarios pueden crear propiedades"}, 403
                
        try:
            # Carga del esquema
            propiedad = propiedad_schema.load(request.json, session = db.session)
            
            # Identificar si el id del usuario, se asocia con el id de la propiedad
            propiedad.id_usuario = current_user.id
            
            # Agregar propiedad
            db.session.add(propiedad)

            # Aplicar cambios
            db.session.commit()
        
        # Retorno de error de validación
        except ValidationError as validation_error:
            return validation_error.messages, 400
        
        # En caso de una excepción
        except exc.IntegrityError as e:

            # Revertir cambios
            db.session.rollback()

            # Retorno de mensaje de error
            return {'mensaje': 'Hubo un error creando la propiedad. Revise los datos proporcionados'}, 400
        
        # Retorno de mensaje de éxito
        return propiedad_schema.dump(propiedad), 201
    
    @jwt_required()
    def get(self): # Método #2

        if current_user.rol == Usuario.ROL_PROPIETARIO:
            propiedades = db.session.execute(
                select(Propiedad).filter(Propiedad.id_usuario == current_user.id)
            ).scalars().all()
        elif current_user.rol == Usuario.ROL_ADMIN:
            propiedades = db.session.execute(
                select(Propiedad).filter(Propiedad.id_admin == current_user.id)
            ).scalars().all()
        else:
            return {"mensaje": "Rol no reconocido"}, 403

        # Retorno de las propiedades
        return propiedad_schema.dump(propiedades, many = True)