# 3rd Party Libraries
from flask import request
from sqlalchemy import exc, select
from flask_restful import Resource
from marshmallow import ValidationError
from vistas.utils import buscar_propiedad
from flask_jwt_extended import current_user, jwt_required
from modelos import ActividadMantenimiento, EstadoMantenimiento, Propiedad, db, ActividadMantenimientoSchema

# Instanciar Elemento Propiedad Esquema
actividad_mantenimiento_schema = ActividadMantenimientoSchema()

class VistaActividadesMantenimiento(Resource):

    @jwt_required()
    def post(self, id_propiedad): 
        
        try:
            # Verificar que la propiedad pertenezca al usuario actual
            propiedad = Propiedad.query.filter_by(id = id_propiedad, id_usuario = current_user.id).first()

            # En caso de no presentar resultados, se arroja un mensaje de error
            if not propiedad:
                return {"mensaje": "Propiedad no encontrada o no autorizada"}, 404

            # Cargar datos del elemento
            nueva_actividad = actividad_mantenimiento_schema.load(request.json, session = db.session)
            
            # Asignar la relación automática (Criterio de la HU)
            nueva_actividad.id_propiedad = id_propiedad
            
            # Agregamos el nuevo elemento
            db.session.add(nueva_actividad)
            
            # Aplicamos cambios
            db.session.commit()

            # Retorno de mensaje de éxito
            return actividad_mantenimiento_schema.dump(nueva_actividad), 201

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
            return {"mensaje": "Error al crear la actividad "}, 500
    
    @jwt_required()
    def get(self, id_propiedad):

        # Filtramos por la primera propiedad
        propiedad = Propiedad.query.filter_by(id = id_propiedad, id_usuario = current_user.id).first()
        
        # Se retorna un error en caso de que no arroje resultados
        if not propiedad:
            return {"mensaje": "No autorizado"}, 401
        
        # Filtramos por los elementos de la propiedad
        actividades = ActividadMantenimiento.query.filter_by(id_propiedad = id_propiedad).all()

        # Retorno de elementos de la propiedad
        return actividad_mantenimiento_schema.dump(actividades, many = True), 200


class VistaActividadMantenimiento(Resource):

    @jwt_required()
    def put(self, id_propiedad, id_actividad):

        try:
            propiedad = Propiedad.query.filter_by(id=id_propiedad, id_usuario=current_user.id).first()
            if not propiedad:
                return {"mensaje": "Propiedad no encontrada o no autorizada"}, 404

            actividad = ActividadMantenimiento.query.filter_by(id=id_actividad, id_propiedad=id_propiedad).first()
            if not actividad:
                return {"mensaje": "Actividad no encontrada"}, 404

            datos = request.json
            nuevo_concepto = datos.get('concepto', actividad.concepto)

            duplicado = ActividadMantenimiento.query.filter(
                ActividadMantenimiento.id_propiedad == id_propiedad,
                ActividadMantenimiento.concepto == nuevo_concepto,
                ActividadMantenimiento.id != id_actividad
            ).first()
            if duplicado:
                return {"mensaje": "Ya existe una actividad con ese concepto en esta propiedad"}, 409

            actividad_actualizada = actividad_mantenimiento_schema.load(
                datos, instance=actividad, session=db.session, partial=True
            )
            actividad_actualizada.id_propiedad = id_propiedad
            db.session.commit()

            return actividad_mantenimiento_schema.dump(actividad_actualizada), 200

        except ValidationError as err:
            return err.messages, 400

        except Exception:
            db.session.rollback()
            return {"mensaje": "Error al editar la actividad"}, 500

    @jwt_required()
    def delete(self, id_propiedad, id_actividad):
        propiedad = Propiedad.query.filter_by(id = id_propiedad, id_usuario = current_user.id).first()
        if not propiedad:
            return {"mensaje": "No autorizado"}, 401

        actividad = ActividadMantenimiento.query.filter_by(id = id_actividad, id_propiedad = id_propiedad).first()
        if not actividad:
            return {"mensaje": "Actividad no encontrada"}, 404

        if actividad.estado == EstadoMantenimiento.EN_PROGRESO:
            return {"mensaje": "No se puede eliminar una actividad en estado En Progreso"}, 400

        db.session.delete(actividad)
        db.session.commit()
        return {"mensaje": "Actividad eliminada exitosamente"}, 200