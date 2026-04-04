# 1st Party Libraries
from app import app
from modelos import Usuario, Propiedad, ElementoPropiedad, Banco, TipoEstado, db

# 3rd Party Libraries
import json
import unittest
from datetime import datetime
from flask_jwt_extended import create_access_token

class TestCrearElemento(unittest.TestCase):
    """"""
    def setUp(self):

        # Configuración del modo de pruebas
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = False
        
        # Creación del cliente
        self.client = self.app.test_client()

        # Creación de la base de pruebas
        with self.app.app_context():
            
            # Creación de la base
            db.create_all()
        
            # Instanciar usuario
            self.usuario = Usuario(usuario = 'Pedro El Escamoso', rol = Usuario.ROL_PROPIETARIO, contrasena = '123456')
            
            # Agregarlo en la base
            db.session.add(self.usuario)
            
            # Aplicar cambios
            db.session.commit()

            # Creación del token
            self.usuario_token = create_access_token(identity = str(self.usuario.id))        

            # Instanciar propiedad
            self.datos_propiedad = Propiedad(nombre_propiedad = 'Paladium', ciudad = 'Bogotá', municipio = 'Cundinamarca',
                                            direccion = 'Calle 75 #4 - 51', nombre_propietario = 'Pedro El Escamoso', numero_contacto = '1234567', 
                                            banco = Banco.BANCOLOMBIA, numero_cuenta = '000033322255599', id_usuario = self.usuario.id)            

            # Agregarlo en la base
            db.session.add(self.datos_propiedad)

            # Aplicar cambios
            db.session.commit()

            # Guardar ID Propiedad
            self.propiedad_id = self.datos_propiedad.id

    def tearDown(self):
        # Eliminación de tablas y registros
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_crear_elemento(self):
        """"""

        # Establecer contexto
        with self.app.app_context():
            
            # Instanciar elemento de la propiedad
            elemento_propiedad = ElementoPropiedad(nombre = 'Jacuzzi', tipo = 'Baño', estado = TipoEstado.EXCELENTE, 
                                                descripcion = 'Bañera de hidromasaje que usa chorros de agua y aire a presión para proporcionar masajes terapéuticos',
                                                fecha_registro = datetime.now(), zona = 'Habitación Principal', id_propiedad = self.datos_propiedad.id)
            
            # Añadir elemento en la propiedad
            db.session.add(elemento_propiedad)
            db.session.commit()

            # Consultar elemento de la base de datos
            elemento = ElementoPropiedad.query.filter_by(nombre = 'Jacuzzi').first()

            # Comparar si el nombre del elemento propiedad coincide con lo ingresado por defecto
            self.assertEqual(elemento.nombre, 'Jacuzzi')
            self.assertEqual(elemento.tipo, 'Baño')

    def test_eliminar_elemento(self):
        
        # Establecer contexto
        with self.app.app_context():

            # Instanciar elemento de la propiedad
            elemento_propiedad = ElementoPropiedad(nombre = 'Jacuzzi', tipo = 'Baño', estado = TipoEstado.EXCELENTE, 
                                                   descripcion = 'Bañera de hidromasaje que usa chorros de agua y aire a presión para proporcionar masajes terapéuticos',
                                                   fecha_registro = datetime.now(), zona = 'Habitación Principal', id_propiedad = self.datos_propiedad.id)
            
            # Añadir elemento en la propiedad
            db.session.add(elemento_propiedad)
            db.session.commit()

            # Obtención del ID
            id_elemento = str(elemento_propiedad.id)

        # Obtención de la URL de la ID de propiedad y elemento
        endpoint = f'/propiedades/{self.datos_propiedad.id}/elementos_propiedad/{id_elemento}'
        headers = {'Authorization': f'Bearer {self.usuario_token}'}

        # Eliminación del registro
        response = self.client.delete(endpoint, headers = headers)

        # Comparación a nivel de status code
        self.assertEqual(response.status_code, 204)

        # Establecer contexto
        with self.app.app_context():

            # Comparación con un registro vacío
            elemento_en_db = db.session.get(ElementoPropiedad, id_elemento)
            self.assertIsNone(elemento_en_db)

if __name__ == '__main__':
    unittest.main()