# 1st Party Libraries
import json
import unittest

# 3rd Party Libraries
from flask_jwt_extended import create_access_token
from modelos import Usuario, CategoriaMovimiento, db


class TestListarCategorias(unittest.TestCase):
    """Pruebas para el listado de categorías de movimientos."""

    def setUp(self):
        """Configurar el entorno de prueba creando usuarios y categorías necesarias."""

        # Instanciar la aplicación Flask
        from app import create_flask_app
        self.app = create_flask_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        # Instanciar usuarios de prueba
        self.usuario_1 = Usuario(usuario = 'usuario_1', rol = Usuario.ROL_PROPIETARIO, contrasena = '123456')
        self.usuario_2 = Usuario(usuario = 'usuario_2', rol = Usuario.ROL_PROPIETARIO, contrasena = '123456')

        # Agregar usuarios a la base de datos
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.commit()

        # Categorías del usuario_1 — deben aparecer en su listado
        self.cat_1 = CategoriaMovimiento(nombre = 'Servicios', id_usuario = self.usuario_1.id)
        self.cat_2 = CategoriaMovimiento(nombre = 'Arriendo',  id_usuario = self.usuario_1.id)

        # Categoría del usuario_2 — NO debe aparecer en el listado del usuario_1
        self.cat_3 = CategoriaMovimiento(nombre = 'Otros', id_usuario = self.usuario_2.id)

        # Agregar categorías a la base de datos
        db.session.add_all([self.cat_1, self.cat_2, self.cat_3])
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

    def actuar(self, token = None):
        """Método para realizar las pruebas del método GET /categorias."""

        # Configurar los encabezados de la solicitud
        headers = {'Content-Type': 'application/json'}

        # Si se proporciona un token de autenticación, lo incluye en los encabezados
        if token:
            headers.update({'Authorization': f'Bearer {token}'})

        # Realizar la solicitud GET a la ruta /categorias
        self.respuesta      = self.client.get('/categorias', headers = headers)

        # Obtener el JSON de la respuesta
        self.respuesta_json = self.respuesta.json

    def test_retorna_200(self):
        """Prueba que se retorna un status code 200 al listar categorías."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que la respuesta sea un status code 200
        self.assertEqual(self.respuesta.status_code, 200)

    def test_retorna_solo_categorias_del_usuario(self):
        """Prueba que el listado solo contiene las categorías del usuario autenticado."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que solo se retornen las 2 categorías del usuario_1
        self.assertEqual(len(self.respuesta_json), 2)

    def test_retorna_categorias_ordenadas_alfabeticamente(self):
        """Prueba que las categorías se retornan ordenadas alfabéticamente."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Extraer los nombres de las categorías retornadas
        nombres = [c['nombre'] for c in self.respuesta_json]

        # Verificar que los nombres estén ordenados alfabéticamente
        self.assertEqual(nombres, sorted(nombres))

    def test_retorna_lista_vacia_si_no_hay_categorias(self):
        """Prueba que se retorna una lista vacía si el usuario no tiene categorías registradas."""

        # Crear un usuario nuevo sin categorías
        usuario_sin_categorias = Usuario(usuario = 'usuario_3', rol = Usuario.ROL_PROPIETARIO, contrasena = '123456')
        db.session.add(usuario_sin_categorias)
        db.session.commit()

        # Crear token del usuario sin categorías
        token = create_access_token(identity = str(usuario_sin_categorias.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que la respuesta sea una lista vacía
        self.assertEqual(self.respuesta_json, [])

    def test_retorna_401_sin_token(self):
        """Prueba que se retorna un status code 401 al intentar listar categorías sin token."""

        # Realizar la solicitud sin token
        self.actuar()

        # Verificar que la respuesta sea un status code 401
        self.assertEqual(self.respuesta.status_code, 401)

# Ejecutar la prueba
if __name__ == '__main__':
    unittest.main(debug = True)