# 1st Party Libraries
import datetime
from modelos import db

# 3rd Party Libraries
import pytest
from app import create_flask_app
from unittest.mock import MagicMock

# Fixtures
@pytest.fixture(autouse = True)

def app():
    """Función para crear la aplicación Flask y configurar la base de datos, JWT y CORS."""
    
    # Instanciar la aplicación Flask
    application = create_flask_app()

    # Confirmación de la base de datos
    application.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": 'sqlite:///admon_reservas_test.db'})

    # Creación de la base de datos
    with application.app_context():
        
        # Crear la base de datos
        db.create_all()

        # Aplicar cambios
        yield application

        # Eliminar la base de datos
        db.session.rollback()

        # Cerrar la sesión de la base de datos
        db.session.close()

        # Eliminar la base de datos
        db.drop_all()

# Fixtures
@pytest.fixture()
def client(app):
    """Función para crear un cliente Flask."""

    # Crear un cliente Flask
    return app.test_client()

# Fixtures
@pytest.fixture()
def mock_datetime_now(monkeypatch):
    """Función para crear una función mock de datetime.datetime.now()."""

    def datetime_mock_func(fake_time):
        """Función mock de datetime.datetime.now()."""

        # Crear una instancia de datetime.datetime
        datetime_mock = MagicMock(wraps = datetime.datetime)

        # Configurar la función mock
        datetime_mock.now.return_value = fake_time

        # Aplicar la función mock
        monkeypatch.setattr(datetime, "datetime", datetime_mock)

    # Retornar la instancia de datetime.datetime
    return datetime_mock_func
