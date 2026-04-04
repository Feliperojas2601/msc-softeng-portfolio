import json

from flask_jwt_extended import create_access_token
from modelos import Banco, ActividadMantenimiento, EstadoMantenimiento, PeriodicidadMantenimiento, TipoCategoriaMantenimiento, Usuario, Propiedad, db


class TestCrearActividadMantanimiento:

    def setup_method(self):
        self.usuario_1 = Usuario(usuario='usuario_1', rol=Usuario.ROL_ADMIN, contrasena='123456')
        self.usuario_2 = Usuario(usuario='usuario_2', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        db.session.add(self.usuario_1)
        db.session.add(self.usuario_2)
        db.session.commit()

        self.propiedad_1_usu_1 = Propiedad(nombre_propiedad='propiedad cerca a la quebrada', ciudad='Boyaca', municipio='Paipa',
                              direccion='Vereda Toibita', nombre_propietario='Jorge Loaiza', numero_contacto='1234567', banco=Banco.BANCOLOMBIA,
                              numero_cuenta='000033322255599', id_usuario=self.usuario_1.id)
        self.propiedad_2_usu_1 = Propiedad(nombre_propiedad='Apto edificio Alto', ciudad='Bogota',
                              direccion='cra 100#7-21 apto 1302', nombre_propietario='Carlos Julio', numero_contacto='666777999', banco=Banco.NEQUI,
                              numero_cuenta='3122589635', id_usuario=self.usuario_1.id)
        db.session.add(self.propiedad_1_usu_1)
        db.session.add(self.propiedad_2_usu_1)
        db.session.commit()

        self.actividad_mantenimiento = {
        'concepto': 'lubricacion',
        'categoria': TipoCategoriaMantenimiento.LIMPIEZA.value,
        'periodicidad': PeriodicidadMantenimiento.MENSUAL.value,
        'estado': EstadoMantenimiento.PROGRAMADO.value,
        'fecha_registro': '2023-01-06',
        'costo': '34455',
        }

    def teardown_method(self):
        db.session.rollback()
        Usuario.query.delete()
        Propiedad.query.delete()
        ActividadMantenimiento.query.delete()

    def actuar(self, client, id_propiedad, actividad_mantenimiento=None, token=None):
        actividad_mantenimiento = actividad_mantenimiento or self.actividad_mantenimiento
        headers = {'Content-Type': 'application/json'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        self.respuesta = client.post(f'/propiedades/{id_propiedad}/actividades_mantenimiento', data=json.dumps(actividad_mantenimiento), headers=headers)
        self.respuesta_json = self.respuesta.json

    def test_retorna_201(self, client):
        token_usuario_1 = create_access_token(identity=str(self.usuario_1.id))
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_1)
        assert self.respuesta.status_code == 201
    
    def test_retorna_movimiento_creado(self, client):
        token_usuario_1 = create_access_token(identity=str(self.usuario_1.id))
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_1)
        assert self.respuesta_json
        assert 'id' in self.respuesta_json
        assert 'concepto' in self.respuesta_json
        assert 'categoria' in self.respuesta_json
        assert 'estado' in self.respuesta_json
        assert 'periodicidad' in self.respuesta_json
        assert 'id_propiedad' in self.respuesta_json

    def test_crea_registro_db(self, client):
        token_usuario_1 = create_access_token(identity=str(self.usuario_1.id))
        self.actuar(client, self.propiedad_1_usu_1.id, token=token_usuario_1)
        assert ActividadMantenimiento.query.filter(ActividadMantenimiento.id == self.respuesta_json['id'],
                                       ActividadMantenimiento.id_propiedad == self.propiedad_1_usu_1.id).one_or_none()