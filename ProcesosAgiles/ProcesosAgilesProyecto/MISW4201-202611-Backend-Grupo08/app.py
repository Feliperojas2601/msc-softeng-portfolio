# 1st Party Libraries
from modelos import Usuario, db
from vistas.login import VistaLogIn
from vistas.bancos import VistaBancos
from vistas.sign_in import VistaSignIn
from vistas.reserva import VistaReserva
from vistas.reservas import VistaReservas
from vistas.categoria import VistaCategoria
from vistas.propiedad import VistaPropiedad
from vistas.movimiento import VistaMovimiento
from vistas.categorias import VistasCategorias
from vistas.movimientos import VistaMovimientos
from vistas.propiedades import VistaPropiedades
from vistas.propietarios import VistaPropietarios
from vistas.tipo_categorias import VistaCategorias
from vistas.tipo_movimientos import VistaTipoMovimientos
from vistas.elemento_propiedad import VistaElementoPropiedad
from vistas.elementos_propiedad import VistaElementosPropiedad
from vistas.estado_mantenimientos import VistaEstadoMantenimientos
from vistas.actividades_mantenimiento import VistaActividadesMantenimiento, VistaActividadMantenimiento
from vistas.tipo_categoria_mantenimientos import VistaTipoCategoriaMantenimientos
from vistas.periodicidad_mantenimientos import VistaPeriodicidadMantenimientos

# 3rd Party Libraries
import os
from flask import Flask
from flask_cors import CORS
from sqlalchemy import select
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Cleaning the app
app = None

def create_flask_app():
    """Función para crear la aplicación Flask y configurar la base de datos, JWT y CORS."""

    # Obtener la ruta absoluta de la carpeta actual
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Instanciar la aplicación Flask
    app = Flask(__name__)

    # Confirmación de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'admon_reservas.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "frase-secreta"
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_IDENTITY_CLAIM"] = "sub"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    # Creación de la base de datos
    db.init_app(app)

    # Creación de la base de datos
    with app.app_context():
        db.create_all()

    # CORS
    CORS(app, resources = {"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Headers", "X-Requested-With"], "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "expose_headers": ["Content-Type", "Authorization"]}})
    
    # Instanciar el gestor de tokens
    jwt = JWTManager(app)
    
    # Callback para la búsqueda de usuarios
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db.session.execute(select(Usuario).filter_by(id = int(identity))).scalar_one_or_none()

    # Agregar las URLs
    add_urls(app)
    
    # Retornar la aplicación
    return app

def add_urls(app):
    """Agregar las URLs a la aplicación Flask."""

    # Instanciar la API RESTful
    api = Api(app)

    # Autorización de usuarios
    api.add_resource(VistaLogIn, "/login")
    api.add_resource(VistaSignIn, "/signin", "/signin/<int:id_usuario>")

    # Enums
    api.add_resource(VistaBancos, "/bancos")
    api.add_resource(VistaTipoMovimientos, "/tipo-movimientos")
    api.add_resource(VistaCategorias, "/tipo-categorias")
    api.add_resource(VistaEstadoMantenimientos, "/estado-mantenimientos")
    api.add_resource(VistaTipoCategoriaMantenimientos, "/tipo-categoria-mantenimientos")
    api.add_resource(VistaPeriodicidadMantenimientos, "/periodicidad-mantenimientos")

    # Propiedades
    api.add_resource(VistaPropiedades, "/propiedades")
    api.add_resource(VistaPropiedad, "/propiedades/<int:id_propiedad>")
    api.add_resource(VistaPropietarios, "/propietarios")

    # Movimientos
    api.add_resource(VistaMovimientos, "/propiedades/<int:id_propiedad>/movimientos")
    api.add_resource(VistaMovimiento, "/movimientos/<int:id_movimiento>")

    # Categorias de movimiento
    api.add_resource(VistasCategorias, '/categorias')
    api.add_resource(VistaCategoria, '/categorias/<int:id_categoria>')
        
    # Reservas
    api.add_resource(VistaReserva, "/reservas/<int:id_reserva>")
    api.add_resource(VistaReservas, "/propiedades/<int:id_propiedad>/reservas")

    # Elementos de propiedad
    api.add_resource(VistaElementoPropiedad, "/propiedades/<int:id_propiedad>/elementos_propiedad/<int:id_elemento>")
    api.add_resource(VistaElementosPropiedad, "/propiedades/<int:id_propiedad>/elementos_propiedad")
    
    # Actividades de mantenimiento
    api.add_resource(VistaActividadesMantenimiento, "/propiedades/<int:id_propiedad>/actividades_mantenimiento")
    api.add_resource(VistaActividadMantenimiento, "/propiedades/<int:id_propiedad>/actividades_mantenimiento/<int:id_actividad>")

# Instanciar la aplicación Flask
app = create_flask_app()

# Iniciar la aplicación Flask
if __name__ == "__main__":

    # Despliegue
    app.run(host = "0.0.0.0", port = 5000, debug = True)
