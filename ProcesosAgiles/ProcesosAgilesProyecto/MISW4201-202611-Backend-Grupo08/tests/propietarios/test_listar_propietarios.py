from flask_jwt_extended import create_access_token
from modelos import Usuario, db


class TestListarPropietarios:

    def setup_method(self):
        self.propietario_1 = Usuario(usuario='propietario_1', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        self.propietario_2 = Usuario(usuario='propietario_2', rol=Usuario.ROL_PROPIETARIO, contrasena='abcdef')
        self.admin = Usuario(usuario='admin_1', rol=Usuario.ROL_ADMIN, contrasena='123456')
        db.session.add(self.propietario_1)
        db.session.add(self.propietario_2)
        db.session.add(self.admin)
        db.session.commit()

    def actuar(self, client, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.get('/propietarios', headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_200_con_lista_de_propietarios(self, client):
        token = create_access_token(identity=str(self.admin.id))
        self.actuar(client, token=token)
        assert self.respuesta.status_code == 200
        assert isinstance(self.respuesta_json, list)
        assert len(self.respuesta_json) == 2
        usuarios = [p['usuario'] for p in self.respuesta_json]
        assert 'propietario_1' in usuarios
        assert 'propietario_2' in usuarios

    def test_respuesta_no_incluye_contrasena(self, client):
        token = create_access_token(identity=str(self.admin.id))
        self.actuar(client, token=token)
        for p in self.respuesta_json:
            assert 'contrasena' not in p
            assert 'id' in p
            assert 'usuario' in p

    def test_retorna_lista_vacia_si_no_hay_propietarios(self, client):
        db.session.delete(self.propietario_1)
        db.session.delete(self.propietario_2)
        db.session.commit()
        token = create_access_token(identity=str(self.admin.id))
        self.actuar(client, token=token)
        assert self.respuesta.status_code == 200
        assert self.respuesta_json == []

    def test_retorna_401_sin_token(self, client):
        self.actuar(client)
        assert self.respuesta.status_code == 401
