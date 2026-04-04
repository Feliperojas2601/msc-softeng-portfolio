import json
import datetime

from flask_jwt_extended import create_access_token
from modelos import (
    Banco,
    ActividadMantenimiento,
    EstadoMantenimiento,
    PeriodicidadMantenimiento,
    TipoCategoriaMantenimiento,
    Usuario,
    Propiedad,
    db,
)


class TestEliminarActividadMantenimiento:

    def setup_method(self):
        self.usuario_propietario = Usuario(usuario='propietario_1', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        self.usuario_otro = Usuario(usuario='propietario_2', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        db.session.add(self.usuario_propietario)
        db.session.add(self.usuario_otro)
        db.session.commit()

        self.propiedad = Propiedad(
            nombre_propiedad='Casa de prueba',
            ciudad='Bogota',
            direccion='Cra 1 #1-1',
            nombre_propietario='Juan Perez',
            numero_contacto='3001234567',
            id_usuario=self.usuario_propietario.id,
        )
        db.session.add(self.propiedad)
        db.session.commit()

        self.actividad_programada = ActividadMantenimiento(
            concepto='Revision general',
            categoria=TipoCategoriaMantenimiento.REVISION,
            periodicidad=PeriodicidadMantenimiento.MENSUAL,
            estado=EstadoMantenimiento.PROGRAMADO,
            fecha_registro=datetime.date(2024, 1, 15),
            costo='50000',
            id_propiedad=self.propiedad.id,
        )
        self.actividad_en_progreso = ActividadMantenimiento(
            concepto='Reparacion techo',
            categoria=TipoCategoriaMantenimiento.REPARACION,
            periodicidad=PeriodicidadMantenimiento.TRIMESTRAL,
            estado=EstadoMantenimiento.EN_PROGRESO,
            fecha_registro=datetime.date(2024, 1, 15),
            costo='200000',
            id_propiedad=self.propiedad.id,
        )
        db.session.add(self.actividad_programada)
        db.session.add(self.actividad_en_progreso)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        ActividadMantenimiento.query.delete()
        Propiedad.query.delete()
        Usuario.query.delete()
        db.session.commit()

    def actuar(self, client, id_propiedad, id_actividad, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        self.respuesta = client.delete(
            f'/propiedades/{id_propiedad}/actividades_mantenimiento/{id_actividad}',
            headers=headers,
        )
        self.respuesta_json = self.respuesta.json

    def test_retorna_200_al_eliminar(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        self.actuar(client, self.propiedad.id, self.actividad_programada.id, token=token)
        assert self.respuesta.status_code == 200

    def test_actividad_eliminada_del_sistema(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        id_actividad = self.actividad_programada.id
        self.actuar(client, self.propiedad.id, id_actividad, token=token)
        assert ActividadMantenimiento.query.filter_by(id=id_actividad).one_or_none() is None

    def test_retorna_400_si_estado_en_progreso(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        self.actuar(client, self.propiedad.id, self.actividad_en_progreso.id, token=token)
        assert self.respuesta.status_code == 400
        assert 'mensaje' in self.respuesta_json

    def test_retorna_404_si_actividad_no_encontrada(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        self.actuar(client, self.propiedad.id, 99999, token=token)
        assert self.respuesta.status_code == 404
        assert 'mensaje' in self.respuesta_json

    def test_retorna_401_si_no_es_propietario(self, client):
        token = create_access_token(identity=str(self.usuario_otro.id))
        self.actuar(client, self.propiedad.id, self.actividad_programada.id, token=token)
        assert self.respuesta.status_code == 401
        assert 'mensaje' in self.respuesta_json
