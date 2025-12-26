# 1st Party Libraries
from .declarative_base import Base

# 3rd Party Libraries
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

class Receta(Base):
    """Especifica los atributos que conforman el modelo en SQLAlchemy de: Receta."""

    # Nombre de la tabla en Receta
    __tablename__ = 'receta'

    # Identificador único de la receta
    id = Column(Integer, primary_key = True)
    # Atributo #1: Nombre de la receta
    nombre = Column(String, nullable = False)
    # Atributo #2: Tiempo de preparción
    tiempo_preparacion = Column(String, nullable = False)
    # Atributo #3: Numero de personas
    numero_personas = Column(Integer, nullable = False)
    # Atributo #4: Porción de Calorias 
    calorias_porcion = Column(Float, nullable = False)
    # Atributo #5: Instrucciones de preparación
    instrucciones_preparacion = Column(String, nullable = False)
    # Relación con RecetaIngrediente (uno a muchos)
    receta_ingredientes = relationship('RecetaIngrediente', back_populates = 'receta', cascade = 'all, delete-orphan')

    def to_dict(self) -> dict:
        """
        Introduccion
        ------------
            - Método que retorna la información de una consulta sobre las recetas disponibles a tipo diccionario.

        Retorna
        -------
            - Recetas: dict.
        """

        # Retorno de una consulta en formato dict
        return {"id": self.id, 
                "nombre": self.nombre, 
                "tiempo": self.tiempo_preparacion,
                "personas": self.numero_personas,
                "calorias": self.calorias_porcion,
                "preparacion": self.instrucciones_preparacion}
    
    def dar_ingredientes(self) -> list[dict]:
        """
        Introducción
        ------------
            - Método que retorna los ingredientes que conforman a una receta.
        
        Retorna
        -------
            - Ingredientes de la receta: list[dict]
        """
        
        # Acceder a los ingredientes a través de la tabla intermedia
        return [{'receta': self.nombre, 
                 'ingrediente': receta_ingrediente.ingrediente.nombre,
                 'cantidad': receta_ingrediente.cantidad_ingrediente, 
                 'unidad': receta_ingrediente.ingrediente.unidad_medida} for receta_ingrediente in self.receta_ingredientes]