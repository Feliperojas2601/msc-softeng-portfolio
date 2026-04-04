import pytest
from modelos import Usuario, Propiedad, Reserva, Movimiento, Banco, TipoMovimiento, db
from vistas.utils import ResultadoBuscar, buscar_propiedad, buscar_reserva, buscar_movimiento


class TestResultadoBuscar:

    def test_entidad_inicializa_en_none(self):
        resultado = ResultadoBuscar()
        assert resultado.entidad is None

    def test_error_inicializa_en_tupla_vacia(self):
        resultado = ResultadoBuscar()
        assert resultado.error == ()

    def test_asignar_entidad(self):
        resultado = ResultadoBuscar()
        resultado.entidad = "objeto_cualquiera"
        assert resultado.entidad == "objeto_cualquiera"

    def test_asignar_error_guarda_codigo_404(self):
        resultado = ResultadoBuscar()
        resultado.error = {'mensaje': 'no encontrado'}, 404
        assert resultado.error[1] == 404

    def test_error_vacio_es_falsy(self):
        resultado = ResultadoBuscar()
        assert not resultado.error

    def test_error_con_valor_es_truthy(self):
        resultado = ResultadoBuscar()
        resultado.error = {'mensaje': 'error'}, 404
        assert resultado.error


class TestBuscarPropiedad:

    def setup_method(self):
        self.propietario = Usuario(usuario='prop_u', rol=Usuario.ROL_PROPIETARIO, contrasena='1234')
        self.otro = Usuario(usuario='otro_u', rol=Usuario.ROL_PROPIETARIO, contrasena='1234')
        self.admin = Usuario(usuario='admin_u', rol=Usuario.ROL_ADMIN, contrasena='1234')
        db.session.add_all([self.propietario, self.otro, self.admin])
        db.session.commit()

        self.propiedad = Propiedad(
            nombre_propiedad='Casa Test', ciudad='Bogotá', direccion='Calle 1',
            nombre_propietario='Test', numero_contacto='111', id_usuario=self.propietario.id
        )
        db.session.add(self.propiedad)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Propiedad.query.delete()
        Usuario.query.delete()
        db.session.commit()

    def test_retorna_entidad_si_propiedad_pertenece_al_propietario(self):
        resultado = buscar_propiedad(self.propiedad.id, self.propietario.id)
        assert resultado.entidad is not None
        assert resultado.entidad.id == self.propiedad.id

    def test_no_hay_error_si_propiedad_encontrada(self):
        resultado = buscar_propiedad(self.propiedad.id, self.propietario.id)
        assert not resultado.error

    def test_retorna_error_404_si_propiedad_no_existe(self):
        resultado = buscar_propiedad(9999, self.propietario.id)
        assert resultado.entidad is None
        assert resultado.error[1] == 404

    def test_retorna_error_404_si_propiedad_no_pertenece_al_usuario(self):
        resultado = buscar_propiedad(self.propiedad.id, self.otro.id)
        assert resultado.entidad is None
        assert resultado.error[1] == 404

    def test_retorna_entidad_si_usuario_es_admin_asignado(self):
        self.propiedad.id_admin = self.admin.id
        db.session.commit()
        resultado = buscar_propiedad(self.propiedad.id, self.admin.id)
        assert resultado.entidad is not None
        assert resultado.entidad.id == self.propiedad.id

    def test_mensaje_error_es_propiedad_no_encontrada(self):
        resultado = buscar_propiedad(9999, self.propietario.id)
        assert resultado.error[0]['mensaje'] == 'propiedad no encontrada'


class TestBuscarReserva:

    def setup_method(self):
        self.propietario = Usuario(usuario='prop_r', rol=Usuario.ROL_PROPIETARIO, contrasena='1234')
        self.otro = Usuario(usuario='otro_r', rol=Usuario.ROL_PROPIETARIO, contrasena='1234')
        db.session.add_all([self.propietario, self.otro])
        db.session.commit()

        self.propiedad = Propiedad(
            nombre_propiedad='Casa Reserva', ciudad='Medellín', direccion='Carrera 2',
            nombre_propietario='Ana', numero_contacto='222', id_usuario=self.propietario.id
        )
        db.session.add(self.propiedad)
        db.session.commit()

        import datetime
        self.reserva = Reserva(
            nombre='Huésped Test',
            fecha_ingreso=datetime.datetime(2024, 6, 1),
            fecha_salida=datetime.datetime(2024, 6, 5),
            plataforma_reserva='Airbnb',
            total_reserva=500000.0,
            comision=50000.0,
            numero_personas=2,
            id_propiedad=self.propiedad.id
        )
        db.session.add(self.reserva)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Reserva.query.delete()
        Propiedad.query.delete()
        Usuario.query.delete()
        db.session.commit()

    def test_retorna_entidad_si_reserva_pertenece_al_propietario(self):
        resultado = buscar_reserva(self.reserva.id, self.propietario.id)
        assert resultado.entidad is not None
        assert resultado.entidad.id == self.reserva.id

    def test_no_hay_error_si_reserva_encontrada(self):
        resultado = buscar_reserva(self.reserva.id, self.propietario.id)
        assert not resultado.error

    def test_retorna_error_404_si_reserva_no_existe(self):
        resultado = buscar_reserva(9999, self.propietario.id)
        assert resultado.entidad is None
        assert resultado.error[1] == 404

    def test_retorna_error_404_si_reserva_no_pertenece_al_usuario(self):
        resultado = buscar_reserva(self.reserva.id, self.otro.id)
        assert resultado.entidad is None
        assert resultado.error[1] == 404

    def test_mensaje_error_es_reserva_no_encontrada(self):
        resultado = buscar_reserva(9999, self.propietario.id)
        assert resultado.error[0]['mensaje'] == 'reserva no encontrada'


class TestBuscarMovimiento:

    def setup_method(self):
        self.propietario = Usuario(usuario='prop_m', rol=Usuario.ROL_PROPIETARIO, contrasena='1234')
        self.otro = Usuario(usuario='otro_m', rol=Usuario.ROL_PROPIETARIO, contrasena='1234')
        db.session.add_all([self.propietario, self.otro])
        db.session.commit()

        self.propiedad = Propiedad(
            nombre_propiedad='Casa Movimiento', ciudad='Cali', direccion='Avenida 3',
            nombre_propietario='Luis', numero_contacto='333', id_usuario=self.propietario.id
        )
        db.session.add(self.propiedad)
        db.session.commit()

        import datetime
        self.movimiento = Movimiento(
            fecha=datetime.datetime(2024, 6, 1),
            concepto='Mantenimiento',
            valor=100000.0,
            tipo_movimiento=TipoMovimiento.EGRESO,
            id_propiedad=self.propiedad.id
        )
        db.session.add(self.movimiento)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        Movimiento.query.delete()
        Propiedad.query.delete()
        Usuario.query.delete()
        db.session.commit()

    def test_retorna_entidad_si_movimiento_pertenece_al_propietario(self):
        resultado = buscar_movimiento(self.movimiento.id, self.propietario.id)
        assert resultado.entidad is not None
        assert resultado.entidad.id == self.movimiento.id

    def test_no_hay_error_si_movimiento_encontrado(self):
        resultado = buscar_movimiento(self.movimiento.id, self.propietario.id)
        assert not resultado.error

    def test_retorna_error_404_si_movimiento_no_existe(self):
        resultado = buscar_movimiento(9999, self.propietario.id)
        assert resultado.entidad is None
        assert resultado.error[1] == 404

    def test_retorna_error_404_si_movimiento_no_pertenece_al_usuario(self):
        resultado = buscar_movimiento(self.movimiento.id, self.otro.id)
        assert resultado.entidad is None
        assert resultado.error[1] == 404

    def test_mensaje_error_es_movimiento_no_encontrado(self):
        resultado = buscar_movimiento(9999, self.propietario.id)
        assert resultado.error[0]['mensaje'] == 'movimiento no encontrado'
