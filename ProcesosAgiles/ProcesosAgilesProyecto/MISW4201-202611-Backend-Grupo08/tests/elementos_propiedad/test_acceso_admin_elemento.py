from datetime import datetime

from flask_jwt_extended import create_access_token
from modelos import Usuario, Propiedad, ElementoPropiedad, Banco, TipoEstado, db, ElementoPropiedadSchema


class TestAccesoAdminElementoPropiedad:

    def setup_method(self):
        self.propietario = Usuario(usuario='propietario_1', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        self.admin = Usuario(usuario='admin_1', rol=Usuario.ROL_ADMIN, contrasena='123456')
        db.session.add(self.propietario)
        db.session.add(self.admin)
        db.session.commit()

        self.propiedad = Propiedad(
            nombre_propiedad='Casa de prueba',
            ciudad='Bogota',
            direccion='Calle 10 #20-30',
            nombre_propietario='Propietario Prueba',
            numero_contacto='3001234567',
            banco=Banco.BANCOLOMBIA,
            numero_cuenta='000111222333',
            id_usuario=self.propietario.id,
            id_admin=self.admin.id
        )
        db.session.add(self.propiedad)
        db.session.commit()

        self.elemento = ElementoPropiedad(
            nombre='Sofá',
            tipo='Sala',
            estado=TipoEstado.BUENO,
            descripcion='Sofá de tres puestos',
            fecha_registro=datetime.now(),
            zona='Sala principal',
            id_propiedad=self.propiedad.id
        )
        db.session.add(self.elemento)
        db.session.commit()

    def teardown_method(self):
        db.session.rollback()
        ElementoPropiedad.query.delete()
        Propiedad.query.delete()
        Usuario.query.delete()

    def test_admin_puede_listar_elementos_via_id_admin(self, client):
        token_admin = create_access_token(identity=str(self.admin.id))
        headers = {'Authorization': f'Bearer {token_admin}'}
        respuesta = client.get(f'/propiedades/{self.propiedad.id}/elementos_propiedad', headers=headers)
        assert respuesta.status_code == 200
        assert isinstance(respuesta.json, list)
        assert len(respuesta.json) == 1

    def test_propietario_puede_listar_elementos(self, client):
        token_propietario = create_access_token(identity=str(self.propietario.id))
        headers = {'Authorization': f'Bearer {token_propietario}'}
        respuesta = client.get(f'/propiedades/{self.propiedad.id}/elementos_propiedad', headers=headers)
        assert respuesta.status_code == 200

    def test_usuario_sin_acceso_no_puede_listar_elementos(self, client):
        otro = Usuario(usuario='otro_usuario', rol=Usuario.ROL_PROPIETARIO, contrasena='123456')
        db.session.add(otro)
        db.session.commit()
        token_otro = create_access_token(identity=str(otro.id))
        headers = {'Authorization': f'Bearer {token_otro}'}
        respuesta = client.get(f'/propiedades/{self.propiedad.id}/elementos_propiedad', headers=headers)
        assert respuesta.status_code == 401

    def test_admin_puede_editar_elemento_via_id_admin(self, client):
        token_admin = create_access_token(identity=str(self.admin.id))
        headers = {'Authorization': f'Bearer {token_admin}', 'Content-Type': 'application/json'}
        payload = {'nombre': 'Sofá actualizado'}
        respuesta = client.put(
            f'/propiedades/{self.propiedad.id}/elementos_propiedad/{self.elemento.id}',
            headers=headers,
            json=payload
        )
        assert respuesta.status_code == 200

    def test_admin_puede_eliminar_elemento_via_id_admin(self, client):
        elemento_borrar = ElementoPropiedad(
            nombre='Lámpara',
            tipo='Decoración',
            estado=TipoEstado.REGULAR,
            descripcion='Lámpara de pie',
            fecha_registro=datetime.now(),
            zona='Sala',
            id_propiedad=self.propiedad.id
        )
        db.session.add(elemento_borrar)
        db.session.commit()
        token_admin = create_access_token(identity=str(self.admin.id))
        headers = {'Authorization': f'Bearer {token_admin}'}
        respuesta = client.delete(
            f'/propiedades/{self.propiedad.id}/elementos_propiedad/{elemento_borrar.id}',
            headers=headers
        )
        assert respuesta.status_code == 204

    def test_admin_puede_crear_elemento_via_id_admin(self, client):
        token_admin = create_access_token(identity=str(self.admin.id))
        headers = {'Authorization': f'Bearer {token_admin}', 'Content-Type': 'application/json'}
        payload = {
            'nombre': 'Mesa',
            'tipo': 'Comedor',
            'estado': TipoEstado.EXCELENTE.value,
            'descripcion': 'Mesa de cuatro puestos',
            'fecha_registro': datetime.now().strftime('%Y-%m-%d'),
            'zona': 'Comedor'
        }
        respuesta = client.post(
            f'/propiedades/{self.propiedad.id}/elementos_propiedad',
            headers=headers,
            json=payload
        )
        assert respuesta.status_code == 201
