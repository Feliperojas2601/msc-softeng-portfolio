from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, Banco, db, PropiedadSchema


class TestObtenerPropiedades:

    def setup_method(self):
        self.admin = Usuario(usuario='admin_1', rol=Usuario.ROL_ADMIN, contrasena='123456')
        self.propietario = Usuario(usuario='propietario_1', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        self.admin_sin_propiedades = Usuario(usuario='admin_2', rol=Usuario.ROL_ADMIN, contrasena='123456')
        db.session.add(self.admin)
        db.session.add(self.propietario)
        db.session.add(self.admin_sin_propiedades)
        db.session.commit()

        # Propiedades del propietario, asignadas al admin
        self.propiedad_1_usu_1 = Propiedad(
            nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
            direccion='Vereda Toibita', nombre_propietario='Jorge Loaiza', numero_contacto='1234567',
            banco=Banco.BANCOLOMBIA, numero_cuenta='000033322255599',
            id_usuario=self.propietario.id, id_admin=self.admin.id
        )
        self.propiedad_2_usu_1 = Propiedad(
            nombre_propiedad='Apto edificio Alto', ciudad='Bogota',
            direccion='cra 100#7-21 apto 1302', nombre_propietario='Carlos Julio',
            numero_contacto='666777999', banco=Banco.NEQUI, numero_cuenta='3122589635',
            id_usuario=self.propietario.id, id_admin=self.admin.id
        )
        # Propiedad del propietario, sin admin asignado
        self.propiedad_1_propietario = Propiedad(
            nombre_propiedad='Apartaestudio', ciudad='Medellin',
            direccion='Cra 25#32-48 apto 305', nombre_propietario='Maria Torres',
            numero_contacto='999999', banco=Banco.DAVIPLATA, numero_cuenta='3114896525',
            id_usuario=self.propietario.id
        )

        db.session.add(self.propiedad_1_usu_1)
        db.session.add(self.propiedad_2_usu_1)
        db.session.add(self.propiedad_1_propietario)
        db.session.commit()

    def actuar(self, client, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.get('/propiedades', headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_lista(self, client):
        token_propietario = create_access_token(identity=str(self.propietario.id))
        self.actuar(client, token=token_propietario)
        assert isinstance(self.respuesta_json, list)

    def test_propietario_retorna_solo_sus_propiedades(self, client):
        token_propietario = create_access_token(identity=str(self.propietario.id))
        self.actuar(client, token=token_propietario)
        schema = PropiedadSchema()
        assert len(self.respuesta_json) == 3
        assert schema.dump(self.propiedad_1_usu_1) in self.respuesta_json
        assert schema.dump(self.propiedad_2_usu_1) in self.respuesta_json
        assert schema.dump(self.propiedad_1_propietario) in self.respuesta_json

    def test_admin_retorna_solo_propiedades_asignadas(self, client):
        token_admin = create_access_token(identity=str(self.admin.id))
        self.actuar(client, token=token_admin)
        schema = PropiedadSchema()
        assert len(self.respuesta_json) == 2
        assert schema.dump(self.propiedad_1_usu_1) in self.respuesta_json
        assert schema.dump(self.propiedad_2_usu_1) in self.respuesta_json

    def test_admin_sin_propiedades_asignadas_retorna_lista_vacia(self, client):
        token_admin_sin_propiedades = create_access_token(identity=str(self.admin_sin_propiedades.id))
        self.actuar(client, token=token_admin_sin_propiedades)
        assert self.respuesta_json == []
        assert self.respuesta.status_code == 200

    def test_retorna_lista_vacia_propietario_sin_propiedades(self, client):
        propietario_sin_propiedades = Usuario(usuario='propietario_2', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        db.session.add(propietario_sin_propiedades)
        db.session.commit()
        token = create_access_token(identity=str(propietario_sin_propiedades.id))
        self.actuar(client, token=token)
        assert self.respuesta_json == []
        assert self.respuesta.status_code == 200

    def test_retorna_401_request_sin_token(self, client):
        self.actuar(client)
        assert self.respuesta.status_code == 401
