from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Banco, db, PropiedadSchema


class TestObtenerPropiedad:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', rol=Usuario.ROL_ADMIN, contrasena='123456')
        self.usuario_2 = Usuario(usuario='usuario_2', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        self.admin = Usuario(usuario='admin_1', rol=Usuario.ROL_ADMIN, contrasena='123456')
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.add(self.admin)
        db.session.commit()

        self.propiedad_1_usu_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', nombre_propietario='Jorge Loaiza', numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        self.propiedad_con_admin = Propiedad(
            nombre_propiedad='Apto con admin', ciudad='Bogota',
            direccion='Cra 10 #20-30', nombre_propietario='Juan Torres',
            numero_contacto='3001234567', banco=Banco.NEQUI, numero_cuenta='3112223344',
            id_usuario=self.usuario_2.id, id_admin=self.admin.id
        )
        db.session.add(self.propiedad_1_usu_1)
        db.session.add(self.propiedad_con_admin)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()
        Propiedad.query.delete()

    def actuar(self, propiedad_id, client, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.get(f'/propiedades/{propiedad_id}', headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_200_si_propiedad_existe_y_es_del_usuario(self, client):
        token_usuario_1 = create_access_token(identity=str(self.usuario_1.id)) 
        self.actuar(self.propiedad_1_usu_1.id, client, token_usuario_1)
        assert self.respuesta.status_code == 200

    def test_retorna_info_propiedad_si_existe_y_es_del_usuario(self, client):
        propiedad_schema = PropiedadSchema()
        token_usuario_1 = create_access_token(identity=str(self.usuario_1.id)) 
        self.actuar(self.propiedad_1_usu_1.id, client, token_usuario_1)
        assert self.respuesta_json == propiedad_schema.dump(self.propiedad_1_usu_1)

    def test_retorna_404_si_propiedad_existe_pero_no_es_del_usuario(self, client):
        token_usuario_2 = create_access_token(identity=str(self.usuario_2.id)) 
        self.actuar(self.propiedad_1_usu_1.id, client, token_usuario_2)
        assert self.respuesta.status_code == 404

    def test_retorna_404_si_propiedad_no_existe(self, client):
        token_usuario_1 = create_access_token(identity=str(self.usuario_1.id)) 
        self.actuar(123, client, token_usuario_1)
        assert self.respuesta.status_code == 404

    def test_retorna_401_no_token(self, client):
        self.actuar(self.propiedad_1_usu_1.id, client)
        assert self.respuesta.status_code == 401

    def test_admin_asignado_retorna_200(self, client):
        token_admin = create_access_token(identity=str(self.admin.id))
        self.actuar(self.propiedad_con_admin.id, client, token_admin)
        assert self.respuesta.status_code == 200

    def test_admin_asignado_retorna_info_propiedad(self, client):
        propiedad_schema = PropiedadSchema()
        token_admin = create_access_token(identity=str(self.admin.id))
        self.actuar(self.propiedad_con_admin.id, client, token_admin)
        assert self.respuesta_json == propiedad_schema.dump(self.propiedad_con_admin)

    def test_admin_no_asignado_retorna_404(self, client):
        admin_otro = Usuario(usuario='admin_otro', rol=Usuario.ROL_ADMIN, contrasena='123456')
        db.session.add(admin_otro)
        db.session.commit()
        token_admin_otro = create_access_token(identity=str(admin_otro.id))
        self.actuar(self.propiedad_con_admin.id, client, token_admin_otro)
        assert self.respuesta.status_code == 404
