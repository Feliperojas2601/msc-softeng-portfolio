# 1st Party Libraries
import json
import unittest
from datetime import datetime

# 3rd Party Libraries
from flask_jwt_extended import create_access_token
from modelos import Usuario, CategoriaMovimiento, Movimiento, TipoMovimiento, Propiedad, Banco, db


class TestEliminarCategoria(unittest.TestCase):
    """Pruebas para la eliminación de categorías de movimientos."""

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

        # Instanciar categoría de prueba
        self.categoria = CategoriaMovimiento(nombre = 'Servicios', id_usuario = self.usuario_1.id)

        # Agregar categoría a la base de datos
        db.session.add(self.categoria)
        db.session.commit()

    def tearDown(self):
        """Limpiar el entorno de prueba eliminando los datos creados."""

        # Revertir cambios pendientes
        db.session.rollback()

        # Eliminar movimientos de la base de datos
        Movimiento.query.delete()

        # Eliminar categorías de movimientos de la base de datos
        CategoriaMovimiento.query.delete()

        # Eliminar propiedades de la base de datos
        Propiedad.query.delete()

        # Eliminar usuarios de la base de datos
        Usuario.query.delete()

        # Aplicar cambios
        db.session.commit()

    def actuar(self, id_categoria = None, token = None):
        """Método para realizar las pruebas del método DELETE /categorias/<id>."""

        # Usar el ID de la categoría de prueba si no se proporciona uno
        id_categoria = id_categoria or self.categoria.id

        # Configurar los encabezados de la solicitud
        headers = {'Content-Type': 'application/json'}

        # Si se proporciona un token de autenticación, lo incluye en los encabezados
        if token:
            headers.update({'Authorization': f'Bearer {token}'})

        # Realizar la solicitud DELETE a la ruta /categorias/<id>
        self.respuesta = self.client.delete(f'/categorias/{id_categoria}', headers = headers)

    def test_retorna_204(self):
        """Prueba que se retorna un status code 204 al eliminar una categoría correctamente."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud
        self.actuar(token = token)

        # Verificar que la respuesta sea un status code 204
        self.assertEqual(self.respuesta.status_code, 204)

    def test_elimina_registro_en_db(self):
        """Prueba que el registro de la categoría se elimina correctamente de la base de datos."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Guardar el ID de la categoría antes de eliminarla
        id_categoria = self.categoria.id

        # Realizar la solicitud
        self.actuar(token = token)

        # Limpiar la caché de la sesión para forzar consulta real a la base de datos
        db.session.expire_all()
        db.session.close()

        # Verificar que la categoría ya no existe en la base de datos
        self.assertIsNone(CategoriaMovimiento.query.filter(CategoriaMovimiento.id ==id_categoria).one_or_none())

    def test_retorna_404_categoria_no_existe(self):
        """Prueba que se retorna un status code 404 al intentar eliminar una categoría que no existe."""

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Realizar la solicitud con un ID que no existe
        self.actuar(id_categoria = 99999, token = token)

        # Verificar que la respuesta sea un status code 404
        self.assertEqual(self.respuesta.status_code, 404)

    def test_retorna_400_categoria_en_uso(self):
        """Prueba que no se puede eliminar una categoría que está asociada a un movimiento."""

        # Crear propiedad necesaria para el movimiento
        propiedad = Propiedad(nombre_propiedad  = 'Casa de prueba', ciudad = 'Bogota', municipio = 'Usaquen', direccion = 'Calle 123', nombre_propietario = 'Usuario Uno', numero_contacto = '3001234567', banco = Banco.BANCOLOMBIA, numero_cuenta = '123456789', id_usuario = self.usuario_1.id)
        db.session.add(propiedad)
        db.session.commit()

        # Crear movimiento asociado a la categoría
        movimiento = Movimiento(fecha = datetime(2024, 1, 1), concepto = 'Pago de servicios', valor = 50000, tipo_movimiento = TipoMovimiento.EGRESO, id_propiedad = propiedad.id, id_categoria = self.categoria.id)
        db.session.add(movimiento)
        db.session.commit()

        # Crear token del usuario_1
        token = create_access_token(identity = str(self.usuario_1.id))

        # Intentar eliminar la categoría que está en uso
        self.actuar(token = token)

        # Verificar que la respuesta sea un status code 400
        self.assertEqual(self.respuesta.status_code, 400)

        # Verificar que el campo 'mensaje' en la respuesta contenga el mensaje de error
        self.respuesta_json = self.respuesta.json
        self.assertTrue('mensaje' in self.respuesta_json)

    def test_retorna_401_sin_token(self):
        """Prueba que se retorna un status code 401 al intentar eliminar una categoría sin token."""

        # Realizar la solicitud sin token
        self.actuar()

        # Verificar que la respuesta sea un status code 401
        self.assertEqual(self.respuesta.status_code, 401)

# Ejecutar la prueba
if __name__ == '__main__':
    unittest.main(debug = True)