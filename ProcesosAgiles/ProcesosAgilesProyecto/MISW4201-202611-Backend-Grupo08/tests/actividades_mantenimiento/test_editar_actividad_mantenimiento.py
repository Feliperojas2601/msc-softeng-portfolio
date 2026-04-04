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


class TestEditarActividadMantenimiento:

    def setup_method(self):
        self.usuario_propietario = Usuario(usuario='propietario_edit_1', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        self.usuario_otro = Usuario(usuario='propietario_edit_2', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        db.session.add(self.usuario_propietario)
        db.session.add(self.usuario_otro)
        db.session.commit()

        self.propiedad = Propiedad(
            nombre_propiedad='Casa de edicion',
            ciudad='Bogota',
            direccion='Cra 2 #2-2',
            nombre_propietario='Ana Torres',
            numero_contacto='3009876543',
            id_usuario=self.usuario_propietario.id,
        )
        db.session.add(self.propiedad)
        db.session.commit()

        self.actividad = ActividadMantenimiento(
            concepto='Limpieza filtros',
            categoria=TipoCategoriaMantenimiento.LIMPIEZA,
            periodicidad=PeriodicidadMantenimiento.MENSUAL,
            estado=EstadoMantenimiento.PROGRAMADO,
            fecha_registro=datetime.date(2024, 3, 1),
            costo='80000',
            id_propiedad=self.propiedad.id,
        )
        self.actividad_existente = ActividadMantenimiento(
            concepto='Revision electrica',
            categoria=TipoCategoriaMantenimiento.REVISION,
            periodicidad=PeriodicidadMantenimiento.TRIMESTRAL,
            estado=EstadoMantenimiento.PROGRAMADO,
            fecha_registro=datetime.date(2024, 3, 1),
            costo='150000',
            id_propiedad=self.propiedad.id,
        )
        db.session.add(self.actividad)
        db.session.add(self.actividad_existente)
        db.session.commit()

        self.datos_edicion = {
            'concepto': 'Limpieza profunda filtros',
            'categoria': TipoCategoriaMantenimiento.LIMPIEZA.value,
            'periodicidad': PeriodicidadMantenimiento.TRIMESTRAL.value,
            'costo': '95000',
        }

    def teardown_method(self):
        db.session.rollback()
        ActividadMantenimiento.query.delete()
        Propiedad.query.delete()
        Usuario.query.delete()
        db.session.commit()

    def actuar(self, client, id_propiedad, id_actividad, datos=None, token=None):
        datos = datos if datos is not None else self.datos_edicion
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        self.respuesta = client.put(
            f'/propiedades/{id_propiedad}/actividades_mantenimiento/{id_actividad}',
            data=json.dumps(datos),
            headers=headers,
        )
        self.respuesta_json = self.respuesta.json

    def test_retorna_200_al_editar(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        self.actuar(client, self.propiedad.id, self.actividad.id, token=token)
        assert self.respuesta.status_code == 200

    def test_retorna_actividad_actualizada(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        self.actuar(client, self.propiedad.id, self.actividad.id, token=token)
        assert self.respuesta_json['concepto'] == self.datos_edicion['concepto']
        assert self.respuesta_json['periodicidad'] == self.datos_edicion['periodicidad']
        assert self.respuesta_json['costo'] == self.datos_edicion['costo']

    def test_persiste_cambios_en_db(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        self.actuar(client, self.propiedad.id, self.actividad.id, token=token)
        actividad_db = ActividadMantenimiento.query.get(self.actividad.id)
        assert actividad_db.concepto == self.datos_edicion['concepto']
        assert actividad_db.costo == self.datos_edicion['costo']

    def test_retorna_409_si_concepto_duplicado(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        datos_duplicados = {
            'concepto': self.actividad_existente.concepto,
            'categoria': TipoCategoriaMantenimiento.LIMPIEZA.value,
            'periodicidad': PeriodicidadMantenimiento.MENSUAL.value,
            'costo': '80000',
        }
        self.actuar(client, self.propiedad.id, self.actividad.id, datos=datos_duplicados, token=token)
        assert self.respuesta.status_code == 409
        assert 'mensaje' in self.respuesta_json

    def test_permite_guardar_mismo_concepto_sin_cambio(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        datos_mismo_concepto = {
            'concepto': self.actividad.concepto,
            'categoria': TipoCategoriaMantenimiento.REVISION.value,
            'periodicidad': PeriodicidadMantenimiento.TRIMESTRAL.value,
            'costo': '99000',
        }
        self.actuar(client, self.propiedad.id, self.actividad.id, datos=datos_mismo_concepto, token=token)
        assert self.respuesta.status_code == 200

    def test_retorna_404_si_actividad_no_encontrada(self, client):
        token = create_access_token(identity=str(self.usuario_propietario.id))
        self.actuar(client, self.propiedad.id, 99999, token=token)
        assert self.respuesta.status_code == 404
        assert 'mensaje' in self.respuesta_json

    def test_retorna_404_si_propiedad_no_autorizada(self, client):
        token = create_access_token(identity=str(self.usuario_otro.id))
        self.actuar(client, self.propiedad.id, self.actividad.id, token=token)
        assert self.respuesta.status_code == 404
        assert 'mensaje' in self.respuesta_json

    def test_retorna_401_sin_token(self, client):
        self.actuar(client, self.propiedad.id, self.actividad.id)
        assert self.respuesta.status_code == 401
