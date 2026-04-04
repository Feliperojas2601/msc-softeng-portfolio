import json
from modelos import Usuario, Propiedad, Banco, db


class TestAsignarAdminPropiedad:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        self.usuario_admin = Usuario(usuario='usuario_admin', rol=Usuario.ROL_ADMIN, contrasena='123456')
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_admin)
        db.session.commit()

        self.propiedad_1 = Propiedad(
            nombre_propiedad='propiedad cerca a la quebrada',
            ciudad='Boyaca',
            municipio='Paipa',
            direccion='Vereda Toibita',
            nombre_propietario='Jorge Loaiza',
            numero_contacto='1234567',
            banco=Banco.BANCOLOMBIA,
            numero_cuenta='000033322255599',
            id_usuario=self.usuario_1.id
        )
        db.session.add(self.propiedad_1)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()

    def actuar(self, datos, propiedad_id, client):
        headers = {'Content-Type': 'application/json'}
        self.respuesta = client.patch(f'/propiedades/{propiedad_id}', data=json.dumps(datos), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_asigna_id_admin_exitosamente(self, client):
        self.actuar({'id_admin': self.usuario_admin.id}, self.propiedad_1.id, client)
        assert self.respuesta.status_code == 200
        assert self.respuesta_json['id_admin'] == self.usuario_admin.id

    def test_retorna_404_si_propiedad_no_existe(self, client):
        self.actuar({'id_admin': self.usuario_admin.id}, 99999, client)
        assert self.respuesta.status_code == 404
        assert self.respuesta_json == {'mensaje': 'propiedad no encontrada'}

    def test_retorna_400_si_body_sin_id_admin(self, client):
        self.actuar({}, self.propiedad_1.id, client)
        assert self.respuesta.status_code == 400
        assert self.respuesta_json == {'mensaje': 'id_admin es requerido'}
