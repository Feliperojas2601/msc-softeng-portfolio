# 3rd Party Libraries
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Conexión al Motor de BD
def get_database_path() -> str:
    """
    Introducción
    ------------
        - Método para determinar dinámicamente dónde crear la base de datos:
        - En tests/ si se está ejecutando unittest o pytest
        - En la raíz del proyecto en otros casos

    Retorna
    -------
        - Ruta: str.
    """
    
    # Verificar si estamos ejecutando tests 
    is_testing = ('unittest' in sys.modules)
    
    # Renombrar la ruta del archivo si se están realizando acciones desde la carpeta tests
    if is_testing:
        return 'tests/recetario.sqlite'
    
    # Renombrar la ruta del archivo si se están realizando acciones por afuera de la carpeta tests
    else:
        return 'recetario.sqlite'

# Configuración del Motor de BD
engine = create_engine(f'sqlite:///{get_database_path()}')

# Creación de sesión
Session = sessionmaker(bind = engine)
session = Session()

# Clase base para la creación de modelos en SQLAlchemy
Base = declarative_base()