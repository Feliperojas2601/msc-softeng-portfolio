import enum
from marshmallow import fields
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class TipoMovimiento(enum.Enum):
    INGRESO = 'INGRESO'
    EGRESO = 'EGRESO'

class TipoEstado(enum.Enum):
    BUENO = 'BUENO'
    MALO = 'MALO'
    REGULAR = 'REGULAR'
    EXCELENTE = 'EXCELENTE'

class Banco(enum.Enum):
    BANCO_BBVA                      = 'BANCO_BBVA'
    BANCAMIA                        = 'BANCAMIA'
    BANCO_AGRARIO                   = 'BANCO_AGRARIO'
    BANCO_AV_VILLAS                 = 'BANCO_AV_VILLAS'
    BANCO_CAJA_SOCIAL               = 'BANCO_CAJA_SOCIAL'
    BANCO_CITIBANK                  = 'BANCO_CITIBANK'
    BANCO_COOPERATIVO_COOPCENTRAL   = 'BANCO_COOPERATIVO_COOPCENTRAL'
    BANCO_CREDIFINANCIERA           = 'BANCO_CREDIFINANCIERA'
    DAVIPLATA                       = 'DAVIPLATA'
    BANCO_DE_BOGOTA                 = 'BANCO_DE_BOGOTA'
    BANCO_DE_OCCIDENTE              = 'BANCO_DE_OCCIDENTE'
    BANCO_FALABELLA                 = 'BANCO_FALABELLA'
    BANCO_FINANDINA                 = 'BANCO_FINANDINA'
    BANCO_GNB_SUDAMERIS             = 'BANCO_GNB_SUDAMERIS'
    BANCO_ITAU                      = 'BANCO_ITAU'
    BANCO_MUNDO_MUJER               = 'BANCO_MUNDO_MUJER'
    BANCO_PICHINCHA                 = 'BANCO_PICHINCHA'
    BANCO_POPULAR                   = 'BANCO_POPULAR'
    BANCO_PROCREDIT                 = 'BANCO_PROCREDIT'
    BANCO_SANTANDER                 = 'BANCO_SANTANDER'
    BANCO_SERFINANZA                = 'BANCO_SERFINANZA'
    BANCO_TEQUENDAMA                = 'BANCO_TEQUENDAMA'
    BANCO_WWB                       = 'BANCO_WWB'
    BANCOLDEX                       = 'BANCOLDEX'
    BANCOLOMBIA                     = 'BANCOLOMBIA'
    BANCOMPARTIR                    = 'BANCOMPARTIR'
    BANCOOMEVA                      = 'BANCOOMEVA'
    COLTEFINANCIERA                 = 'COLTEFINANCIERA'
    CONFIAR_COOPERATIVA_FINANCIERA  = 'CONFIAR_COOPERATIVA_FINANCIERA'
    COOFIANTIOQUIA                  = 'COOFIANTIOQUIA'
    COOFINEP_COOPERATIVA_FINANCIERA = 'COOFINEP_COOPERATIVA_FINANCIERA'
    COTRAFA_COOPERATIVA_FINANCIERA  = 'COTRAFA_COOPERATIVA_FINANCIERA'
    FINANCIERA_JURISCOOP            = 'FINANCIERA_JURISCOOP'
    GIROS_Y_FINANZAS_CF             = 'GIROS_Y_FINANZAS_CF'
    IRIS                            = 'IRIS'
    LULO_BANK                       = 'LULO_BANK'
    MOVii                           = 'MOVii'
    SCOTIABANK_COLPATRIA            = 'SCOTIABANK_COLPATRIA'
    SERVIFINANSA                    = 'SERVIFINANSA'
    RAPPIPAY                        = 'RAPPIPAY'
    NEQUI                           = 'NEQUI'

class TipoMovimientoCategoria(enum.Enum):
    INGRESOS_RESERVAS = 'INGRESOS RESERVAS'
    INGRESOS_ADICIONALES = 'INGRESOS ADICIONALES'
    COMISIONES = 'COMISIONES'
    LIMPIEZA = 'LIMPIEZA'
    MANTENIMIENTO = 'MANTENIMIENTO'
    REPARACIONES = 'REPARACIONES'
    IMPUESTOS = 'IMPUESTO'

class TipoCategoriaMantenimiento(enum.Enum):
    LIMPIEZA = 'LIMPIEZA'
    REPARACION = 'REPARACION'
    REVISION = 'REVISION'
    
class EstadoMantenimiento(enum.Enum):
    PROGRAMADO = 'PROGRAMADO'
    EN_PROGRESO = 'EN PROGRESO'
    FINALIZADO = 'FINALIZADO'
    CANCELADO = 'CANCELADO'

class PeriodicidadMantenimiento(enum.Enum):
    EVENTO = 'EVENTO'
    MENSUAL = 'MENSUAL'
    TRIMESTRAL = 'TRIMESTRAL'

class Propiedad(db.Model):
    __tablename__ = 'propiedad'
    __table_args__ = (UniqueConstraint('direccion', 'ciudad', 'municipio', name = 'unique_address'),)

    id = db.Column(db.Integer, primary_key = True)
    nombre_propiedad = db.Column(db.String(128), nullable = False)
    ciudad = db.Column(db.String(128), nullable = False)
    municipio = db.Column(db.String(128), nullable = True)
    direccion = db.Column(db.String(128), nullable = False)
    nombre_propietario = db.Column(db.String(128), nullable = False)
    numero_contacto = db.Column(db.String(15), nullable = False)
    banco = db.Column(db.Enum(Banco), nullable = True)
    numero_cuenta = db.Column(db.String(32), nullable = True)
    movimientos = db.relationship('Movimiento', cascade = 'all, delete, delete-orphan')
    reservas = db.relationship('Reserva', cascade = 'all, delete, delete-orphan')
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False)
    id_admin = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = True)

class Reserva(db.Model):
    __tablename__ = 'reserva'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(128), nullable = False)
    fecha_ingreso = db.Column(db.DateTime, nullable = False)
    fecha_salida = db.Column(db.DateTime, nullable = False)
    plataforma_reserva = db.Column(db.String(50), nullable = False)
    total_reserva = db.Column(db.Float, nullable = False)
    comision = db.Column(db.Float, nullable = False)
    numero_personas = db.Column(db.Integer, nullable = False, default = 0)
    observaciones = db.Column(db.String(128))
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'))
    movimientos = db.relationship('Movimiento', cascade = 'all, delete, delete-orphan')

class CategoriaMovimiento(db.Model):
    __tablename__ = 'categoria_movimiento'
    __table_args__ = (UniqueConstraint('nombre', 'id_usuario', name = 'unique_categoria_nombre'),)

    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(64), nullable = False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable = False)

class Movimiento(db.Model):
    __tablename__ = 'movimiento'
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime, nullable = False)
    concepto = db.Column(db.String(128), nullable = False)
    valor = db.Column(db.Float, nullable = False)
    id_reserva = db.Column(db.Integer, db.ForeignKey('reserva.id'), nullable = True)
    tipo_movimiento = db.Column(db.Enum(TipoMovimiento), nullable = False)
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria_movimiento.id'), nullable = True)

    # Definir conceptos como constantes para proteger la consistencia de los datos
    CONCEPTO_RESERVA = 'RESERVA'
    CONCEPTO_COMISION = 'COMISION'

class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = (UniqueConstraint('usuario', name = 'unique_username'),)
    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(50), nullable = False)
    rol = db.Column(db.String(20), nullable = False)
    contrasena = db.Column(db.String(50), nullable = False)
    propiedades = db.relationship('Propiedad', foreign_keys='Propiedad.id_usuario', cascade = 'all, delete, delete-orphan')
    
    # Definir roles como constantes para proteger la consistencia de los datos
    ROL_PROPIETARIO = 'PROPIETARIO'
    ROL_ADMIN = 'ADMIN'

class ElementoPropiedad(db.Model):
    __tablename__ = 'elemento_propiedad'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(40), nullable = False)
    tipo = db.Column(db.String(40), nullable = False)
    estado = db.Column(db.Enum(TipoEstado), nullable = False)
    descripcion = db.Column(db.String(125), nullable = False)
    fecha_registro = db.Column(db.Date, nullable = False)
    zona = db.Column(db.String(80), nullable = False)
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'), nullable = False)

class ActividadMantenimiento(db.Model):
    __tablename__ = 'actividad_mantenimiento'
    id = db.Column(db.Integer, primary_key = True)
    concepto = db.Column(db.String(40), nullable = False)
    categoria = db.Column(db.Enum(TipoCategoriaMantenimiento), nullable = True)
    periodicidad = db.Column(db.Enum(PeriodicidadMantenimiento), nullable = False)
    estado = db.Column(db.Enum(EstadoMantenimiento), nullable = True)
    fecha_registro = db.Column(db.Date, nullable = False)
    costo = db.Column(db.String(40), nullable = False)
    id_propiedad = db.Column(db.Integer, db.ForeignKey('propiedad.id'), nullable = False)

class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        include_relationships = True
        include_fk = True
        load_instance = True

class PropiedadSchema(SQLAlchemyAutoSchema):
    banco = fields.Enum(Banco, by_value = True, allow_none = True)
    id_usuario = fields.Integer(dump_only = True)
    id_admin = fields.Integer(dump_only = True, allow_none = True)
    class Meta:
        model = Propiedad
        include_relationships = True
        include_fk = True
        load_instance = True

class ElementoPropiedadSchema(SQLAlchemyAutoSchema):
    estado = fields.Enum(TipoEstado, by_value = True)
    fecha_registro = fields.Date(format = '%Y-%m-%d')
    id_propiedad = fields.Int(dump_only = True)
    class Meta:
        model = ElementoPropiedad
        include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = db.session

class MovimientoSchema(SQLAlchemyAutoSchema):
    tipo_movimiento = fields.Enum(TipoMovimiento, by_value = True)
    id_reserva = fields.Integer(allow_none = True)
    id_propiedad = fields.Integer()
    id_categoria = fields.Integer(allow_none = True)
    
    class Meta:
        model = Movimiento
        include_relationships = True
        load_instance = True

class CategoriaMovimientoSchema(SQLAlchemyAutoSchema):
    id_usuario = fields.Integer(dump_only=True)
    class Meta:
        model = CategoriaMovimiento
        include_fk = True
        load_instance = True
        sqla_session = db.session

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ('contrasena',)

class ActividadMantenimientoSchema(SQLAlchemyAutoSchema):
    categoria = fields.Enum(TipoCategoriaMantenimiento, by_value = True)
    estado = fields.Enum(EstadoMantenimiento, by_value = True)
    periodicidad = fields.Enum(PeriodicidadMantenimiento, by_value = True)
    fecha_registro = fields.Date(format = '%Y-%m-%d')
    id_propiedad = fields.Int(dump_only = True)
    class Meta:
        model = ActividadMantenimiento
        include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = db.session
