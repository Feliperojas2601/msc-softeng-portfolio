import json
from faker import Faker
from flask import request
from flask import current_app
from sqlalchemy import text
from modelos import Usuario, db
from flask_jwt_extended import create_access_token

class TestCrearUsuario:

    def setup_method(self):
        db.session.rollback()
        db.session.query(Usuario).delete()
        db.session.commit()

        self.data_factory = Faker()
        user1 = self.data_factory.uuid4()
        user2 = self.data_factory.uuid4()

        self.datos_nuevo_usuario1 = {
            'id': 1,
            'username': user1,
            'role': Usuario.ROL_PROPIETARIO,
            'password': self.data_factory.word()
        }
        self.datos_nuevo_usuario2 = {
            'id': 2,
            'username': user2,
            'role': Usuario.ROL_PROPIETARIO,
            'password': self.data_factory.word()
        }

    def teardown_method(self):
        db.session.rollback()
        db.session.query(Usuario).delete()
        db.session.commit()

    def actuar(self, nuevo_usuario_info, client):
        self.respuesta = client.post('/signin', data=json.dumps(nuevo_usuario_info), headers={'Content-Type': 'application/json'})
        self.respuesta_json = self.respuesta.json

    def test_crear_usuario_responde_201(self, client):
        self.actuar(self.datos_nuevo_usuario2, client)
        print("STATUS:", self.respuesta.status_code)
        print("JSON:", self.respuesta_json)
        print("RESP:", self.respuesta.status_code, self.respuesta_json)
        assert self.respuesta.status_code == 201

    def test_crear_usuario_mismo_usuario_retorna_400(self, client):
        usuario = Usuario(usuario='usuario_test', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        db.session.add(usuario)
        db.session.commit()

        self.datos_nuevo_usuario1.update({'username': 'usuario_test'})
        self.actuar(self.datos_nuevo_usuario1, client)
        assert self.respuesta.status_code == 400

    def test_retorna_campos_esperados(self, client):
        self.actuar(self.datos_nuevo_usuario2, client)
        assert 'token' in self.respuesta_json
        assert 'id' in self.respuesta_json
        assert 'mensaje' in self.respuesta_json

    def test_crea_usuario_en_db(self, client):
        self.actuar(self.datos_nuevo_usuario2, client)
        usuario_db = Usuario.query.filter(Usuario.usuario == self.datos_nuevo_usuario2['username']).all()
        assert len(usuario_db) == 1

class TestActualizarUsuario:
    
    def setup_method(self):
        self.usuario = Usuario(usuario='test_user', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        db.session.add(self.usuario)
        db.session.commit()

        self.usuario_token = create_access_token(identity=str(self.usuario.id))
        self.usuario_info = {'username': 'usuario_cambiado', 'role': Usuario.ROL_PROPIETARIO, 'password': 'nueva_contrasena'}

    def teardown_method(self):
        db.session.rollback()
        db.session.query(Usuario).delete()
        db.session.commit()

    def actuar(self, client, usuario_info=None, usuario_id=None, token=None):
        usuario_info = usuario_info or self.usuario_info
        usuario_id = usuario_id or self.usuario.id
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})

        self.respuesta = client.put(f'/signin/{usuario_id}', data=json.dumps(usuario_info), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_actualizar_usuario_solo_actualiza_contrasena(self, client):
        self.actuar(client, token=self.usuario_token)
        db.session.expire_all()
        usuario_db = Usuario.query.filter(Usuario.id == self.usuario.id).first()
        assert usuario_db.usuario != 'usuario_cambiado'
        assert usuario_db.usuario == 'test_user'
        assert usuario_db.contrasena == 'nueva_contrasena'

    def test_retorna_400_si_token_usuario_no_coincide_con_usuario_id_en_url(self, client):
        self.actuar(client, usuario_id=1234, token=self.usuario_token)
        assert self.respuesta.status_code == 400
        assert self.respuesta_json == {"mensaje": "Peticion invalida"}

    def test_retorna_401_si_token_no_es_enviado(self, client):
        self.actuar(client)
        assert self.respuesta.status_code == 401

    def test_retorna_200_si_actualizacion_exitosa(self, client):
        self.actuar(client, token=self.usuario_token)
        assert self.respuesta.status_code == 200

    def test_retorna_campos_esperados(self, client):
        self.actuar(client, token=self.usuario_token)
        assert 'usuario' in self.respuesta_json
        assert 'id' in self.respuesta_json
        assert 'propiedades' in self.respuesta_json
