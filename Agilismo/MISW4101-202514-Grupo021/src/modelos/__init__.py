# Import all models to ensure they are available when SQLAlchemy initializes
from .declarative_base import Base, engine, session
from .Receta import Receta
from .Ingrediente import Ingrediente
from .RecetaIngrediente import RecetaIngrediente

# Ensure all models are available
__all__ = ['Base', 'engine', 'session', 'Receta', 'Ingrediente', 'RecetaIngrediente']