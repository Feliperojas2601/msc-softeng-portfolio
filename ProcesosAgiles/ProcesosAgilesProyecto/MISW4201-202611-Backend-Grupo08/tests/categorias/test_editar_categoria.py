# 1st Party Libraries
import json
import unittest

# 3rd Party Libraries
from flask_jwt_extended import create_access_token
from modelos import Usuario, CategoriaMovimiento, db


class TestEditarCategoria(unittest.TestCase):
    """Pruebas para la edición de categorías de movimientos."""

    def setUp(self):
        """Configurar el entorno de prueba creando usuarios y categorías necesarias."""

        # Instanciar la aplicación Flask
        from app import create_flask_app
        self.app = create_flask_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Instanciar usuario de prueba
        self.usuario_1 = Usuario(usuario = 'usuario_1', rol = Usuario.ROL_PROPIETARIO, contrasena = '123456')

        # Agregar usuario a la base de datos
        db.session.add(self.usuario_1)
        db.session.commit()

        # Instanciar categorías de prueba
        self.categoria_1 = CategoriaMovimiento(nombre = 'Servicios', id_usuario = self.usuario_1.id)
        self.categoria_2 = CategoriaMovimiento(nombre = 'Arriendo',  id_usuario = self.usuario_1.id)

        # Agregar categorías a la base de datos
        db.session.add_all([self.categoria_1, self.categoria_2])
        db.session.commit()

    def tearDown(self):
        """Limpiar el entorno de prueba eliminando los datos creados."""

        # Revertir cambios pendientes
        db.session.rollback()

        # Eliminar categorías de movimientos de la base de datos
        CategoriaMovimiento.query.delete()

        # Eliminar usuarios de la base de datos
        Usuario.query.delete()

        # Aplicar cambios
        db.session.commit()

    def actuar(self, id_categoria = None, body = None, token = None):
        """Método para realizar las pruebas del método PUT /categorias/<id>."""

        # Usar el ID de la categoría_1 si no se proporciona uno
        id_categoria = id_categoria or self.categoria_1.id

        # Usar un nombre válido por defecto si no se proporciona body
        body = body or {'nombre': 'Servicios Publicos'}

        # Configurar los encabezados de la solicitud
        headers = {'Content-Type': 'application/json'}

        # Si se proporciona un token de autenticación, lo incluye en los encabezados
        if token:
            headers.update({'Authorization': f'Bearer {token}'})

        # Realizar la solicitud PUT a la ruta /categorias/<id>
        self.respuesta      = self.client.put(f'/categorias/{id_categoria}', data = json.dumps(body), headers = headers)

        # Obtener el JSON de la respuesta
        self.respuesta_json = self.respuesta.json

    def test_retorna_200(self):
        """Prueba que se retorna un status code 200 al editar una categoría correctamente."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que la respuesta sea un status code 200
        self.assertEqual(self.respuesta.status_code, 200)

    def test_actualiza_nombre_en_respuesta(self):
        """Prueba que la respuesta refleja el nombre actualizado de la categoría."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que el nombre en la respuesta sea el nuevo nombre
        self.assertEqual(self.respuesta_json['nombre'], 'Servicios Publicos')

    def test_actualiza_nombre_en_db(self):
        """Prueba que el nombre de la categoría se actualiza correctamente en la base de datos."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Guardar el ID antes de cerrar la sesión
        id_categoria = self.categoria_1.id

        # Realizar la solicitud
        self.actuar(token = token)

        # Limpiar la caché de la sesión para forzar consulta real a la base de datos
        db.session.expire_all()
        db.session.close()

        # Verificar que el nombre en la base de datos sea el nuevo nombre
        categoria_actualizada = CategoriaMovimiento.query.filter(CategoriaMovimiento.id == id_categoria).one_or_none()
        
        # Verificar que el nombre en la base de datos sea el nuevo nombre
        self.assertEqual(categoria_actualizada.nombre, 'Servicios Publicos')

    def test_retorna_409_nombre_duplicado(self):
        """Prueba que se retorna un status code 409 al intentar editar una categoría con un nombre que ya existe."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Intentar renombrar 'Servicios' a 'Arriendo' que ya existe
        self.actuar(body = {'nombre': 'Arriendo'}, token = token)

        # Verificar que la respuesta sea un status code 409
        self.assertEqual(self.respuesta.status_code, 409)

        # Verificar que el campo 'mensaje' en la respuesta contenga el mensaje de error
        self.assertTrue('mensaje' in self.respuesta_json)

    def test_retorna_400_nombre_vacio(self):
        """Prueba que se retorna un status code 400 al intentar editar una categoría con un nombre vacío."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud con nombre vacío
        self.actuar(body = {'nombre': ''}, token = token)

        # Verificar que la respuesta sea un status code 400
        self.assertEqual(self.respuesta.status_code, 400)

        # Verificar que el campo 'mensaje' en la respuesta contenga el mensaje de error
        self.assertTrue('mensaje' in self.respuesta_json)

    def test_retorna_400_caracteres_especiales(self):
        """Prueba que se retorna un status code 400 al intentar editar una categoría con caracteres especiales."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud con caracteres especiales
        self.actuar(body = {'nombre': 'Servicios@#!'}, token = token)

        # Verificar que la respuesta sea un status code 400
        self.assertEqual(self.respuesta.status_code, 400)

        # Verificar que el campo 'mensaje' en la respuesta contenga el mensaje de error
        self.assertTrue('mensaje' in self.respuesta_json)

    def test_retorna_404_categoria_no_existe(self):
        """Prueba que se retorna un status code 404 al intentar editar una categoría que no existe."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud con un ID que no existe
        self.actuar(id_categoria = 99999, token = token)

        # Verificar que la respuesta sea un status code 404
        self.assertEqual(self.respuesta.status_code, 404)

    def test_retorna_401_sin_token(self):
        """Prueba que se retorna un status code 401 al intentar editar una categoría sin token."""

        # Realizar la solicitud sin token
        self.actuar()

        # Verificar que la respuesta sea un status code 401
        self.assertEqual(self.respuesta.status_code, 401)

# Ejecutar la prueba
if __name__ == '__main__':
    unittest.main(debug = True)