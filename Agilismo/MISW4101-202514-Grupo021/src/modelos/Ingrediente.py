# 1st Party Libraries
from .declarative_base import Base

# 3rd Party Libraries
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

class Ingrediente(Base):
    """Especifica los atributos que conforman el modelo en SQLAlchemy de: Ingrediente."""

    # Nombre de la tabla en Ingrediente
    __tablename__ = 'ingrediente'

    # Identificador Unico del ingrediente
    id = Column(Integer, primary_key = True)
    # Atributo #1: Nombre del ingrediente
    nombre = Column(String, nullable = False)
    # Atributo #2: Unidad de medida
    unidad_medida = Column(String, nullable = False)
    # Atributo #3: Valor por unidad
    valor_unidad = Column(Float, nullable = False)
    # Atributo #4: Sitio de compra 
    sitio_compra = Column(String, nullable = False)
    # Relación con RecetaIngrediente (uno a muchos)
    receta_ingredientes = relationship('RecetaIngrediente', back_populates = 'ingrediente')

    def to_dict(self) -> dict:
        """
        Introduccion
        ------------
            - Método que retorna la información de una consulta sobre las ingredientes disponibles a tipo diccionario.

        Retorna
        -------
            - Ingredientes: dict.
        """

        # Retorno de una consulta en formato dict
        return {"id": self.id, 
                "nombre": self.nombre, 
                "unidad": self.unidad_medida,
                "valor": self.valor_unidad,
                "sitioCompra": self.sitio_compra}