# 3rd Party Libraries
import traceback
from flask import request
from sqlalchemy import exc
from flask_restful import Resource
from modelos import db, Usuario, UsuarioSchema
from flask_jwt_extended import create_access_token, current_user, jwt_required

# Instanciar usuario esquema
usuario_schema = UsuarioSchema()

class VistaSignIn(Resource):
    """Clase que lleva a cabo procesos de actualización y registro de usuarios."""

    def post(self): # Método #1
        """
        Introducción
        ------------
            - Metodo que lleva a cabo el registro de usuarios nuevos.
        
        Parámetros
        ----------
            - Sin parámetros.
        
        Retorna
        -------
            - dict: Mensaje de error o confirmación.
        """
        
        # Instanciar nuevo usuario
        nuevo_usuario = Usuario(usuario = request.json.get("username"), rol = request.json.get("role"), contrasena = request.json.get("password"))
        
        # Intento de registro
        try:
            # Registrar usuario en la base de datos
            db.session.add(nuevo_usuario)

            # Aplicar cambios
            db.session.commit()
        
        # Revertir en caso de errores
        except exc.IntegrityError:
            db.session.rollback()

            # Retorno del mensaje de error
            return {"mensaje": "Ya existe un usuario con este identificador"}, 400
        
        # Capturar otro error
        except Exception as e: 
            
            # Revertir errores
            db.session.rollback()
            print("********************************")
            
            # Presentación del error
            print(f"ERROR REAL DETECTADO: {str(e)}")
            
            # Generación del output del errpr
            traceback.print_exc() 

            print("********************************")

            # Retorno del error de mensaje
            return {"mensaje": f"Error interno: {str(e)}"}, 500
        
        # Creación del token de acceso
        token_de_acceso = create_access_token(identity = str(nuevo_usuario.id))

        # Retorno del mensaje de éxito
        return {"mensaje": "usuario creado", "token": token_de_acceso, "id": nuevo_usuario.id}, 201

    @jwt_required()
    def put(self, id_usuario): # Método #2
        """
        Introducción
        ------------
            - Método que permite la actualización llevada a cabo por un usuario.
        
        Parámetros
        ----------
            - id_usuario: int, sin valores por defecto.

        Retorna
        -------
            - object: Creación del usuario
        """
        
        # Obtención del usuario token
        usuario_token = current_user

        # Confirmación del ID del usuario
        if id_usuario != current_user.id:
            return {"mensaje": "Peticion invalida"}, 400
        
        # Obtención del token usuario contraseña
        usuario_token.contrasena = request.json.get("password", usuario_token.contrasena)
        
        # Aplicación de cambios
        db.session.commit()

        # Retorno de la operación
        return usuario_schema.dump(usuario_token)
