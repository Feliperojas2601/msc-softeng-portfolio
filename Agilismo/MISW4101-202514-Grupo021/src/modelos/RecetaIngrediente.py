# 1st Party Libraries
from .declarative_base import Base

# 3rd Party Libraries
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey

class RecetaIngrediente(Base):
    """Especifica los atributos que conforman el modelo en SQLAlchemy de: RecetaIngrediente."""

    # Nombre de la tabla en RecetaIngrediente
    __tablename__ = 'receta_ingrediente'

    # Identificador único
    id = Column(Integer, primary_key = True)
    # Atributo #1: Cantidad del ingrediente
    cantidad_ingrediente = Column(Float, nullable = False)
    
    # Llaves foráneas
    id_receta = Column(Integer, ForeignKey('receta.id'), nullable = False)
    id_ingrediente = Column(Integer, ForeignKey('ingrediente.id'), nullable = False)

    # Definición de las relaciones para poder acceder a los objetos relacionados (recetas y ingredientes)
    receta = relationship('Receta', back_populates = 'receta_ingredientes')
    ingrediente = relationship('Ingrediente', back_populates = 'receta_ingredientes')