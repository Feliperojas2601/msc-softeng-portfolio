# 1st Party Libraries
import json
import unittest

# 3rd Party Libraries
from flask_jwt_extended import create_access_token
from modelos import Usuario, CategoriaMovimiento, db


class TestCrearCategoria(unittest.TestCase):
    """Pruebas para la creación de categorías de movimientos."""

    def setUp(self):
        """Configurar el entorno de prueba creando usuarios y datos necesarios."""
        
        # Instanciar la aplicación Flask
        from app import create_flask_app
        self.app = create_flask_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Instanciar usuarios de prueba
        self.usuario_1  =  Usuario(usuario = 'usuario_1', rol = Usuario.ROL_PROPIETARIO, contrasena = '123456')
        self.usuario_2  =  Usuario(usuario = 'usuario_2', rol = Usuario.ROL_PROPIETARIO, contrasena = '123456')
        
        # Agregar usuarios a la base de datos
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.commit()

        # Datos de prueba para la creación de una categoría válida
        self.categoria_valida  =  {'nombre': 'Servicios'}

    def tearDown(self):
        """Limpiar el entorno de prueba eliminando los datos creados."""
        
        # Eliminar usuarios de la base de datos
        db.session.rollback()

        # Eliminar categorías de movimientos de la base de datos
        CategoriaMovimiento.query.delete()

        # Eliminar usuarios de la base de datos
        Usuario.query.delete()

        # Aplicar cambios
        db.session.commit()

    def actuar(self, categoria = None, token = None):
        """Método para realizar las pruebas del método POST /categorias."""
        # Obtener los datos de la categoría
        categoria  =  categoria or self.categoria_valida

        # Configurar los encabezados de la solicitud, incluyendo el token de autenticación si se proporciona
        headers  =  {'Content-Type': 'application/json'}
        
        # Si se proporciona un token de autenticación, lo incluye en los encabezados
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        
        # Realizar la solicitud POST a la ruta /categorias con los datos de la categoría
        self.respuesta  =  self.client.post('/categorias', data = json.dumps(categoria), headers = headers)
        
        # Obtener el JSON de la respuesta
        self.respuesta_json  =  self.respuesta.json

    def test_retorna_201(self):
        """Prueba que se retorna un status code 201 al crear una categoría válida."""

        # Crear una categoría válida
        token  =  create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que la respuesta sea un status code 201
        self.assertEqual(self.respuesta.status_code, 201)

    def test_retorna_categoria_creada(self):
        """Prueba que se retorna la categoría creada correctamente."""

        # Crear una categoría válida
        token  =  create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)
        
        # Verificar que la respuesta tenga los campos 'id' y 'nombre'
        self.assertTrue('id' in self.respuesta_json)
        self.assertTrue('nombre' in self.respuesta_json)

        # Verificar que el campo 'nombre' en la respuesta sea igual al nombre de la categoría creada
        self.assertEqual(self.respuesta_json['nombre'], 'Servicios')

    def test_crea_registro_en_db(self):
        """Prueba que se crea un registro en la base de datos al crear una categoría válida."""

        # Crear una categoría válida
        token  =  create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que se cree un registro en la base de datos
        self.assertIsNotNone(CategoriaMovimiento.query.filter(CategoriaMovimiento.id == self.respuesta_json['id'], CategoriaMovimiento.id_usuario == self.usuario_1.id).one_or_none())

    def test_retorna_401_sin_token(self):
        """Prueba que se retorna un status code 401 al intentar crear una categoría sin token de autenticación."""
        
        # Realizar la solicitud
        self.actuar()

        # Verificar que la respuesta sea un status code 401
        self.assertEqual(self.respuesta.status_code, 401)

    def test_retorna_409_nombre_duplicado(self):
        """Prueba que se retorna un status code 409 al intentar crear una categoría con el mismo nombre que ya existe."""

        # Crear una categoría válida
        token  =  create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)
        
        # Intentar crear la misma categoría de nuevo
        self.actuar(token = token)

        # Verificar que la respuesta sea un status code 409
        self.assertEqual(self.respuesta.status_code, 409)

        # Verificar que el campo 'mensaje' en la respuesta contenga el mensaje de error
        self.assertTrue('mensaje' in self.respuesta_json)

    def test_permite_mismo_nombre_diferente_usuario(self):
        """Prueba que se permite crear una categoría con el mismo nombre si el usuario es diferente."""
        
        # Crear dos usuarios diferentes
        token_1  =  create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token_1)

        # Verificar que la respuesta sea un status code 201
        self.assertEqual(self.respuesta.status_code, 201)

        # usuario_2 también puede crear "Servicios" sin conflicto
        token_2  =  create_access_token(identity = str(self.usuario_2.id))
        
        # Realizar la solicitud
        self.actuar(token = token_2)

        # Verificar que la respuesta sea un status code 201
        self.assertEqual(self.respuesta.status_code, 201)

    def test_retorna_400_nombre_vacio(self):
        """Prueba que se retorna un status code 400 al intentar crear una categoría con un nombre vacío."""
        
        # Crear una categoría válida
        token  =  create_access_token(identity = str(self.usuario_1.id))
        
        # Realizar la solicitud
        self.actuar(categoria = {'nombre': ''}, token = token)
        
        # Verificar que la respuesta sea un status code 400
        self.assertEqual(self.respuesta.status_code, 400)
        
        # Verificar que el campo 'mensaje' en la respuesta contenga el mensaje de error
        self.assertTrue('mensaje' in self.respuesta_json)

    def test_retorna_400_caracteres_especiales(self):
        """Prueba que se retorna un status code 400 al intentar crear una categoría con caracteres especiales."""
        
        # Crear una categoría válida
        token  =  create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(categoria = {'nombre': 'Servicios@#!'}, token = token)
        
        # Verificar que la respuesta sea un status code 400
        self.assertEqual(self.respuesta.status_code, 400)

        # Verificar que el campo 'mensaje' en la respuesta contenga el mensaje de error
        self.assertTrue('mensaje' in self.respuesta_json)

# Ejecutar la prueba
if __name__ == '__main__':
    unittest.main(debug = True)