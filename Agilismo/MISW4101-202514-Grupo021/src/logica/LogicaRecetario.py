# 1st Party Libraries
from src.modelos.Receta import Receta
from src.logica.LogicaMock import LogicaMock
from ..modelos.declarative_base import session
from src.modelos.Ingrediente import Ingrediente
from ..modelos.declarative_base import Base, engine
from src.modelos.RecetaIngrediente import RecetaIngrediente

# 3rd Party Libraries
from sqlalchemy import func

class LogicaRecetario(LogicaMock):
    """Clase que permite la creación, edición y eliminación de recetas. No requiere de un constructor para su creación."""

    def __init__(self) -> None: # Consructor
        """Constructor que hereda de los atributos de la clase LogicaMock."""

        # Heredar listados disponibles traidos de la clase padre LogicaMoch
        super().__init__()

        # Instrucción de creación de BD
        Base.metadata.create_all(engine)

        # Listado de items vacios
        self.listado_vacios = [[], None, '', -1]
    
    def es_entero(self, string) -> bool: # Método #1
        """
        Introducción
        ------------
            - Método que permite arrojar un resultado booleano: True/False en caso de poderse o no realizar un cambio del tipo de dato a int.
        
        Parámetros
        ----------
            - string: str, sin valores por defecto.

        Retorna
        -------
            - True/False: bool.
        """

        # Intento de cambio de tipo de dato a float
        try: 
            int(string) 
            return True 
        
        # Manejo del ValueError a False
        except ValueError: 
            return False

    def es_float(self, string: str) -> bool: # Método #2
        """
        Introducción
        ------------
            - Método que permite arrojar un resultado booleano: True/False en caso de poderse o no realizar un cambio del tipo de dato a float.
        
        Parámetros
        ----------
            - string: str, sin valores por defecto.

        Retorna
        -------
            - True/False: bool.
        """

        # Intento de cambio de tipo de dato a float
        try:
            float(string)
            return True
        
        # Manejo del ValueError a False
        except ValueError:
            return False

    def validar_crear_editar_receta(self, id_receta: int, receta: str, tiempo: str, personas: str, calorias: str, preparacion: str) -> str: # Método #3
        """
        Introducción
        ------------
            - Método que permite identificar la presencia de elementos vacíos en cada uno de los parámetros que conforman a la función.
        
        Parámetros
        ----------
            - id_receta: int, identificador único de la receta, sin valores por defecto.
            - receta: str, nombre de la receta, sin valores por defecto.
            - tiempo: str, tiempo de preparación de la receta, sin valores por defecto.
            - personas: str, número de personas, sin valores por defecto.
            - calorias: str, número de calorías, sin valores por defecto.
            - preparación: str, instrucciones de preparación, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error: str.
        """
    
        # Identificar presencia de vacíos en los campos
        if receta in self.listado_vacios or tiempo in self.listado_vacios or personas in self.listado_vacios or calorias in self.listado_vacios or preparacion in self.listado_vacios:
           return "Hay datos vacíos."
        
        # Identificar presencia de datos ingresados con un formato incorrecto
        elif not isinstance(receta, str) or not isinstance(tiempo, str) or len(tiempo.split(':')) != 3 or self.es_entero(personas) == False or self.es_float(calorias) == False or not isinstance(preparacion, str):
            return "Hay tipos de datos inválidos."

        elif id_receta not in self.listado_vacios:
            return self.validar_editar_receta(id_receta = id_receta, receta = receta)
        
        # Identificar si la receta a agregar ya se encuentra dentro del listado
        elif receta in [receta.nombre for receta in session.query(Receta).filter(Receta.nombre == receta).all()]:
            return "Ya existe una receta con ese nombre."
        
        # En caso de no haber problemas, retorna un ""
        return ""

    def validar_editar_receta(self, id_receta: int, receta: str) -> str: # Método #3.1
        """
        Introducción
        ------------
            - Método que permite validar la edición de una receta, con una validación de nombre existente diferente.

        Parámetros
        ----------
            - id_receta: int, identificador único de la receta, sin valores por defecto.
            - receta: str, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error: str.
        """

        # Informar proceso de edición de la receta
        print('Validando edición de receta...')

        # Traer todos las recetas disponibles
        listado_recetas = session.query(Receta).all()

        # Filtrar Receta por indice
        recetas = listado_recetas[id_receta] if id_receta < len(listado_recetas) else None

        # En caso de que no se encuentren registros
        if recetas in self.listado_vacios:
            return "La receta no existe."

        # Identificar si el nombre de la receta a editar ya se encuentra dentro del listado, diferente a la receta que se está editando
        elif receta in [receta.nombre for receta in session.query(Receta).filter(Receta.nombre == receta, Receta.id != recetas.id).all()]:
            return "Ya existe una receta con ese nombre."

        # En caso de no haber problemas, retorna un ""
        return ""

    def crear_receta(self, receta: str, tiempo: str, personas: str, calorias: str, preparacion: str) -> str: # Método #4
        """
        Introducción
        ------------
            - Método que permite la creación de recetas en SQLite en la base Receta.
        
        Parámetros
        ----------
            - receta: str, nombre de la receta, sin valores por defecto.
            - tiempo: str, tiempo de preparación de la receta, sin valores por defecto.
            - personas: str, número de personas, sin valores por defecto.
            - calorias: str, número de calorías, sin valores por defecto.
            - preparación: str, instrucciones de preparación, sin valores por defecto.
        
        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Instanciar Receta
        nueva_receta = Receta(nombre = receta, tiempo_preparacion = tiempo, numero_personas = personas, calorias_porcion = calorias, instrucciones_preparacion = preparacion)
        
        # Agregar Receta
        session.add(nueva_receta)

        # Aplicar cambios
        session.commit()

        # Retorno del mensaje de éxito de creacíón de la receta
        return "Receta creada exitosamente."
    
    def dar_recetas(self) -> list[dict]: # Método #5
        """
        Introducción
        ------------
            - Método que retorna el listado de recetas disponibles.
        
        Retorna
        -------
            - Listado Recetas: list.
        """

        # Retorno del listado de recetas
        return [receta.to_dict() for receta in session.query(Receta).all()]
    
    def dar_receta(self, id_receta: int) -> dict: # Método #5.1
        """
        Introducción
        ------------
            - Retorna una receta dado su id

        Parámetros:
            - id_receta: int, identificador único de la receta, sin valores por defecto.

        Retorna:
            (dict): La receta identificada con el id_receta recibido como parámetro
        """

        # Traer todos las recetas disponibles
        listado_recetas = session.query(Receta).all()

        # Filtrar Receta por indice
        receta = listado_recetas[id_receta] if id_receta < len(listado_recetas) else None
        
        # Retorno de una receta en formato dict o {} si no se encuentra
        return receta.to_dict() if receta else {}

    def dar_ingredientes_receta(self, id_receta: int) -> list: # Método #6
        """
        Introducción
        ------------
            - Método que retorna el listado de ingredientes que conforman una receta.
        
        Parámetros
        ----------
            - id_receta: int
        
        Retorna
        -------
            - Listado Ingredientes: list[dict]
        """

        # Traer todos las recetas disponibles
        listado_recetas = session.query(Receta).all()

        # Filtrar Receta por indice
        receta = listado_recetas[id_receta] if id_receta < len(listado_recetas) else []

        # En caso de que no se encuentren registros
        if receta == []:
            return []
        
        # Retorno de los ingredientes que conforman a una receta
        return receta.dar_ingredientes()

    def validar_crear_editar_ingrediente(self, nombre: str, unidad: str, valor: str, sitioCompra: str, esCreacion: bool) -> str: # Método #7
        """
        Introducción
        ------------
            - Método que permite validar la creación o edición de un ingrediente.

        Parámetros
        ----------
            - nombre: str, nombre del ingrediente, sin valores por defecto.
            - unidad: str, unidad de medida del ingrediente, sin valores por defecto.
            - valor: str, valor del ingrediente, sin valores por defecto.
            - sitioCompra: str, sitio de compra del ingrediente, sin valores.

        Retorna
        -------
            - Mensaje de Error: str.
        """

        # Identificar presencia de vacíos en los campos
        if nombre in self.listado_vacios or unidad in self.listado_vacios or valor in self.listado_vacios or sitioCompra in self.listado_vacios:
            return "Hay datos vacíos."
        
        # Identificar presencia de datos ingresados con un formato incorrecto
        elif not isinstance(nombre, str) or not isinstance(unidad, str) or self.es_float(valor) == False or not isinstance(sitioCompra, str):
            return "Hay tipos de datos inválidos."
        
        # Detecta si ya existe un ingrediente con ese nombre
        elif nombre in [ingrediente.nombre for ingrediente in session.query(Ingrediente).filter(Ingrediente.nombre == nombre).all()] and esCreacion:
            return "Ya existe un ingrediente con ese nombre."

        # En caso de no haber problemas, retorna un ""
        return ""

    def crear_ingrediente(self, nombre: str, unidad: str, valor: str, sitioCompra: str) -> str: # Método #8
        """
        Introducción
        ------------
            - Método que permite crear un ingrediente en la base de datos.

        Parámetros
        ----------
            - nombre:  str, nombre del ingrediente, sin valores por defecto.
            - unidad: str, unidad de medida del ingrediente, sin valores por defecto.
            - valor: str, valor del ingrediente, sin valores por defecto.
            - sitioCompra: str, sitio de compra del ingrediente, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Instanciar el ingrediente
        nuevo_ingrediente = Ingrediente(nombre = nombre, unidad_medida = unidad, valor_unidad = valor, sitio_compra = sitioCompra)
        
        # Registrar ingrediente
        session.add(nuevo_ingrediente)
        
        # Guardar cambios
        session.commit()

        # Retorno del mensaje de éxito de creación del ingrediente
        return "Ingrediente creado exitosamente."
    
    def eliminar_ingrediente(self, id_ingrediente: int) -> str: # Método #9
        """
        Introduccion
        ------------
            - Método que elimina un ingrediente del listado de ingredientes disponibles.
        
        Parámetros
        ----------
            - id_ingrediente: int, 
        
        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Identificar si no se encuentran ingredientes disponibles
        if session.query(Ingrediente).all() == []:
            return "No hay ingredientes para eliminar."
        
        # Traer todos los ingredientes disponibles
        listado_ingredientes = session.query(Ingrediente).all()

        # Filtrar Ingrediente por indice
        ingrediente = listado_ingredientes[id_ingrediente] if id_ingrediente < len(listado_ingredientes) else None

        # En caso de que no se encuentren ingredientes disponibles
        if ingrediente in self.listado_vacios:
            return "El ingrediente no existe."
        
        # En caso de que el Ingrediente se encuentre en una receta
        elif session.query(RecetaIngrediente).filter(RecetaIngrediente.id_ingrediente == ingrediente.id).first() not in self.listado_vacios:
            return "El ingrediente no puede ser eliminado porque está siendo utilizado en una receta."
        
        # Proceso de eliminación de un Ingrediente
        else: 
            
            # Eliminación del ingrediente
            session.delete(ingrediente)
            
            # Guardar cambios 
            session.commit()

            # Retorno de mensaje de eliminación de ingrediente éxitosamente
            return "Ingrediente eliminado exitosamente."
            
    def dar_ingredientes(self) -> list: # Método #10
        """
        Introduccion
        ------------
            - Método que retorna el listado de ingredientes disponibles de la base Ingrediente.
            - Brinda información adicional con base a los atributos que conforman al modelo ingrediente.

        Retorna
        -------
            - Listado ingredientes: dict.
        """

        # Retorno del listado de recetas
        return [ingrediente.to_dict() for ingrediente in session.query(Ingrediente).all()]

    def validar_crear_editar_ingReceta(self, receta: dict, ingrediente: dict, cantidad: str) -> str: # Método #11
        """
        Introducción
        ------------
            - Método que permite validar la creación o edición de un ingrediente en una receta.

        Parámetros
        ----------
            - receta: str, nombre de la receta, sin valores por defecto.
            - ingrediente: str, nombre del ingrediente, sin valores por defecto.
            - cantidad: str, cantidad del ingrediente, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error: str.
        """

        # Validar que el id de la receta y que el ingrediente no estén vacíos
        if receta == {} or 'id' not in receta:
            return "La receta no tiene id."
        
        # Validar que el id del ingrediente y que el ingrediente no estén vacíos
        elif ingrediente == {} or 'id' not in ingrediente:
            return "El ingrediente no tiene id."
        
        # Validar que la cantidad no esté vacía y sea un número positivo
        elif self.es_float(cantidad) == False or float(cantidad) <= 0:
            return "Hay datos inválidos."

        # Validar que la receta y el ingrediente existen en la BD
        if session.query(Receta).filter(Receta.id == receta['id']).count() == 0:
            return "La receta no existe."
        
        # Validar que el ingrediente y el ingreddiente de la receta existen en la BD
        elif session.query(Ingrediente).filter(Ingrediente.id == ingrediente['id']).count() == 0:
            return "El ingrediente no existe."
        
        # En caso de que el proceso sea éxitoso
        return ""

    def agregar_ingrediente_receta(self, receta: dict, ingrediente: dict, cantidad: str) -> str: # Método #12
        """
        Introducción
        ------------
            - Método que permite agregar un ingrediente a una receta.

        Parámetros
        ----------
            - receta: str, nombre de la receta, sin valores por defecto.
            - ingrediente: str, nombre del ingrediente, sin valores por defecto.
            - cantidad: str, cantidad del ingrediente, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Agregar el ingrediente a la receta
        nuevo_ingrediente_receta = RecetaIngrediente(id_receta = receta['id'], id_ingrediente = ingrediente['id'], cantidad_ingrediente = cantidad)
        
        # Agregar ingrediente
        session.add(nuevo_ingrediente_receta)
        
        # Guardar Cambios
        session.commit()

        # Retorno del mensaje de éxito de creación del ingrediente en la receta
        return "Ingrediente agregado a la receta exitosamente."

    def eliminar_receta(self, id_receta: int) -> str: # Método #13
        """
        Introducción
        ------------
            - Método que permite eliminar una receta del listado de recetas disponibles.

        Parámetros
        ----------
            - id_receta: int, identificador único de la receta, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Traer todos las recetas disponibles
        listado_recetas = session.query(Receta).all()

        # Identificar si no se encuentran recetas disponibles
        if listado_recetas == []:
            return "No hay recetas para eliminar."

        # Filtrar Receta por indice
        receta = listado_recetas[id_receta] if id_receta < len(listado_recetas) else None

        # En caso de que no se encuentren la receta
        if receta in self.listado_vacios:
            return "La receta no existe."

        # Proceso de eliminación de una Receta
        else: 
            
            # Eliminación de la receta
            session.delete(receta)
            
            # Guardar cambios 
            session.commit()

            # Retorno de mensaje de eliminación de receta éxitosamente
            return "Receta eliminada exitosamente."

    def editar_ingrediente_receta(self, id_ingrediente_receta: int, receta: dict, ingrediente: dict, cantidad: str) -> str: # Método #14
        """
        Introducción
        ------------
            - Método que permite editar un ingrediente en una receta.

        Parámetros
        ----------
            - id_ingrediente_receta: int, identificador único del ingrediente en una receta, sin valores por defecto.
            - receta: str, nombre de la receta, sin valores por defecto.
            - ingrediente: str, nombre del ingrediente, sin valores por defecto.
            - cantidad: str, cantidad del ingrediente, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Traer todos los ingredientes en recetas disponibles
        listado_ingredientes_receta = session.query(RecetaIngrediente).all()

        # Filtrar Ingrediente Receta por indice
        ingrediente_receta = listado_ingredientes_receta[id_ingrediente_receta] if id_ingrediente_receta < len(listado_ingredientes_receta) else None

        # En caso de que no se encuentren el ingrediente en la receta
        if ingrediente_receta in self.listado_vacios:
            return "El ingrediente en la receta no existe."

        # Editar el ingrediente en la receta, solo la cantidad
        ingrediente_receta.cantidad_ingrediente = cantidad

        # Guardar cambios
        session.commit()

        # Retorno de mensaje de edición de ingrediente en receta éxitosamente
        return "Ingrediente en la receta editado exitosamente."
    
    def eliminar_ingrediente_receta(self, id_ingrediente_receta: str, receta: object | dict | str) -> str: # Método #16
        """
        Introducción
        ------------
            - Método que permite eliminar el ingrediente de una receta.

        Parámetros
        ----------
            - id_ingrediente_receta: int, identificador único del ingrediente en una receta, sin valores por defecto.
            - receta: str, nombre de la receta, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Realizar búsqueda de receta en caso de ser un diccionario
        if isinstance(receta, dict):
            
            # Si la llave ID se encuentra en receta
            if 'id' in receta:
                busqueda_receta = session.query(Receta).filter(Receta.id == receta['id']).first()
            
            # Si la llave nombre se encuentra en receta
            elif 'nombre' in receta:
                busqueda_receta = session.query(Receta).filter(Receta.nombre == receta['nombre']).first()

        # Realizar búsqueda de receta en caso de ser un texto
        elif isinstance(receta, str):
            busqueda_receta = session.query(Receta).filter(Receta.nombre == receta).first()
        
        # No aplicar cambios si la receta esta instanciada como clase
        elif isinstance(receta, Receta):
            busqueda_receta = receta

        # En caso de que no haya resultados de búsqueda
        if busqueda_receta is None:
            return "La receta no existe."
        
        # Ingredientes de una receta
        ingredientes_receta = session.query(RecetaIngrediente).filter(RecetaIngrediente.id_receta == busqueda_receta.id).all()
        
        # En caso de que no se encuentren ingredientes dentro de la receta
        if ingredientes_receta == []:
            return "No hay ingredientes en la receta para eliminar."

        # Filtrar Ingrediente por indice
        ingrediente = ingredientes_receta[id_ingrediente_receta] if id_ingrediente_receta < len(ingredientes_receta) else None
        
        # Proceso de eliminación del ingrediente den una receta
        session.delete(ingrediente)

        # Aplicar cambios
        session.commit()

        # Retorno del mensaje de éxito
        return "Ingrediente de receta eliminado exitosamente."

    def editar_ingrediente(self, id_ingrediente: int, nombre: str, unidad: str, valor: str, sitioCompra: str) -> str: # Método #15
        """
        Introducción
        ------------
            - Método que permite editar un ingrediente del listado de ingredientes disponibles.

        Parámetros
        ----------
            - id_ingrediente: int, sin valores por defecto.
            - nombre: str, nombre del ingrediente, sin valores por defecto.
            - unidad: str, unidad de medida del ingrediente, sin valores por defecto.
            - valor: str, valor del ingrediente, sin valores por defecto.
            - sitioCompra: str, sitio de compra del ingrediente, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Traer todos los ingredientes disponibles
        listado_ingredientes = session.query(Ingrediente).all()

        if listado_ingredientes == []:
            return "No hay ingredientes para editar."

        # Filtrar Ingrediente por indice
        ingrediente = listado_ingredientes[id_ingrediente] if id_ingrediente < len(listado_ingredientes) else None

        # En caso de que no se encuentren el ingrediente
        if ingrediente in self.listado_vacios:
            return "El ingrediente no existe."

        # Traer las recetas que contienen el ingrediente
        recetas_con_ingrediente = session.query(RecetaIngrediente).filter(RecetaIngrediente.id_ingrediente == ingrediente.id).all()

        # En caso de que el ingrediente se encuentre en una receta, no se puede editar
        if recetas_con_ingrediente != []:
            return "El ingrediente se encuentra agregado en una receta."

        # Edición del ingrediente
        ingrediente.nombre = nombre
        ingrediente.valor_unidad = valor
        ingrediente.unidad_medida = unidad
        ingrediente.sitio_compra = sitioCompra
        
        # Agregar Cambios
        session.add(ingrediente)

        # Guardar cambios
        session.commit()

        # Retorno de mensaje de edición de ingrediente éxitosamente
        return "Ingrediente actualizado exitosamente."

    def editar_receta(self, id_receta: int, receta: str, tiempo: str, personas: int, calorias: int, preparacion: str) -> str: # Método #16
        """
        Introducción
        ------------
            - Método que permite editar una receta existente.

        Parámetros
        ----------
            - id_receta: int, identificador único de la receta, sin valores por defecto.
            - receta: str, nombre de la receta, sin valores por defecto.
            - tiempo: str, tiempo de preparación de la receta, sin valores por defecto.
            - personas: int, número de personas que sirve la receta, sin valores por defecto.
            - calorias: int, número de calorías de la receta, sin valores por defecto.
            - preparacion: str, instrucciones de preparación de la receta, sin valores por defecto.

        Retorna
        -------
            - Mensaje de Error/Éxito: str.
        """

        # Traer todas las recetas disponibles
        listado_recetas = session.query(Receta).all()

        # Filtrar Receta por indice
        receta_obj = listado_recetas[id_receta] if id_receta < len(listado_recetas) else None

        # Edición de la receta
        receta_obj.nombre = receta
        receta_obj.tiempo_preparacion = tiempo
        receta_obj.numero_personas = personas
        receta_obj.calorias_porcion = calorias
        receta_obj.instrucciones_preparacion = preparacion

        # Guardar cambios
        session.commit()

        # Retorno de mensaje de edición de receta exitosamente
        return "Receta actualizada exitosamente."
    
    def dar_preparacion(self, id_receta: int, personas: int) -> str: # Método #17
        """
        Introducción
        ------------
            - Método que proporciona toda la información correspondiente a una receta y realiza los siguientes calculos:
                - Tiempo de preparación.
                - Cantidad de ingredientes.
                - Costo de preparación.
        """

        # Traer todas las recetas disponibles
        listado_recetas = session.query(Receta).all()

        # En caso de que el listado se encuentre vacío
        if listado_recetas in self.listado_vacios:
            return "No hay recetas para preparar."
        
        # En caso de que el usuario haya ingresado un tipo de dato inválido sobre el número de personas
        elif not isinstance(personas, int):
            return "Hay datos inválidos."
        
        # Filtro de receta por indice
        receta = listado_recetas[id_receta] if id_receta < len(listado_recetas) else None

        # En caso de que no hayan resultados por ID
        if receta in self.listado_vacios:
            return "La receta no existe."
        
        # Calcular las calorias y costos proporcionales a las personas
        calorias_proporcionales = self.dar_calorias_proporcionales(calorias_porcion = receta.calorias_porcion, personas_a_preparar = personas, personas_base = receta.numero_personas)
        costo_total_proporcional = self.dar_costo_proporcional(id_receta = receta.id, personas_a_preparar = personas, personas_base = receta.numero_personas)

        # Calcular el tiempo de preparación según las fórmulas 
        tiempo_preparacion_formulado = self.dar_tiempo_preparacion_formulado(receta.tiempo_preparacion, personas, receta.numero_personas)

        # Retorno de la preparación de la receta
        return {'receta': receta.nombre,
                'personas': personas,
                'calorias': calorias_proporcionales,
                'costo': costo_total_proporcional,
                'tiempo_preparacion': tiempo_preparacion_formulado,
                'datos_ingredientes': [{**receta_ingrediente.ingrediente.to_dict(), 'cantidad': receta_ingrediente.cantidad_ingrediente} for receta_ingrediente in session.query(RecetaIngrediente).filter(RecetaIngrediente.id_receta == receta.id).all()]}

    def dar_calorias_proporcionales(self, calorias_porcion: int, personas_a_preparar: int, personas_base: int) -> float: # Método #17.1
        """
        Introducción
        ------------
            - Método que permite calcular las calorías proporcionales según el número de personas.

        Parámetros
        ----------
            - calorias_porcion: int, número de calorías por porción, sin valores por defecto.
            - personas: int, número de personas, sin valores por defecto.

        Retorna
        -------
            - Calorías proporcionales: float.
        """

        # Cálculo de las calorías proporcionales
        return round(calorias_porcion * personas_a_preparar / personas_base, 0)

    def dar_costo_proporcional(self, id_receta: int, personas_a_preparar: int, personas_base: int) -> float: # Método #17.2
        """
        Introducción
        ------------
            - Método que permite calcular el costo proporcional según el número de personas.

        Parámetros
        ----------
            - id_receta: int, identificador único de la receta, sin valores por defecto.
            - personas: int, número de personas, sin valores por defecto.

        Retorna
        -------
            - Costo proporcional: float.
        """
        
        # Cálculo costo base
        costo_base = session.query(func.coalesce(func.sum(RecetaIngrediente.cantidad_ingrediente * Ingrediente.valor_unidad), 0.0)).join(Ingrediente, RecetaIngrediente.id_ingrediente == Ingrediente.id).filter(RecetaIngrediente.id_receta == id_receta).scalar()

        # Retorno costo base por el número de personas a preparar
        return round((float(costo_base) * personas_a_preparar) / personas_base, 0)

    def dar_tiempo_preparacion_formulado(self, tiempo_preparacion: str, personas_a_preparar: int, personas_base: int) -> str: # Método #17
        """
        Introducción
        ------------
            - Método que permite calcular el tiempo de preparación según el número de personas.

        Parámetros
        ----------
            - tiempo_preparacion: str, tiempo de preparación en formato HH:MM:SS, sin valores por defecto.
            - personas: int, número de personas, sin valores por defecto.

        Retorna
        -------
            - Tiempo de preparación formulado: str.
        """

        # Si el número de personas a preparar es menor al número de personas base
        if (personas_a_preparar <= personas_base):
            # Tiempo total en segundos
            tiempo_total_segundos = self.dar_tiempo_total_en_segundos(tiempo_preparacion)

            # Factor de Ajuste
            factor_ajuste = (personas_base - personas_a_preparar) / (2 * personas_base)

            # Ajuste segundos
            tiempo_ajustado_segundos = tiempo_total_segundos - (factor_ajuste * tiempo_total_segundos)
            tiempo_ajustado_segundos = max(0, int(tiempo_ajustado_segundos))

            # Segundos, horas y minutos ajustados
            return self.reconstruir_tiempo_a_formato(tiempo_ajustado_segundos)
        
        # Si el número de personas a preparar es mayor al número de personas base
        else:
            # Tiempo total en segundos
            tiempo_total_segundos = self.dar_tiempo_total_en_segundos(tiempo_preparacion)

            personas_adicionales = personas_a_preparar - personas_base
            grupos_adicionales = personas_adicionales // personas_base
            tiempo_adicional_por_grupo = (2 * tiempo_total_segundos) / 100
            tiempo_adicional_total = grupos_adicionales * tiempo_adicional_por_grupo

            # Tiempo ajustado segundos
            tiempo_ajustado_segundos = tiempo_total_segundos + tiempo_adicional_total
            tiempo_ajustado_segundos = max(0, int(tiempo_ajustado_segundos))

            # Segundos, horas y minutos ajustados
            return self.reconstruir_tiempo_a_formato(tiempo_ajustado_segundos)
        
    def dar_tiempo_total_en_segundos(self, tiempo_preparacion: str) -> int: # Método #18
        """
        Introducción
        ------------
            - Método que permite convertir un tiempo en formato HH:MM:SS a segundos.

        Parámetros
        ----------
            - tiempo_preparacion: str, tiempo de preparación en formato HH:MM:SS, sin valores por defecto.

        Retorna
        -------
            - Tiempo total en segundos: int.
        """

        # Separar tiempo por :
        tiempo_partes = tiempo_preparacion.split(':')

        # Horas, minutos y segundos
        horas = int(tiempo_partes[0])
        minutos = int(tiempo_partes[1])
        segundos = int(tiempo_partes[2])

        # Retorno del tiempo total en segundos
        return horas * 3600 + minutos * 60 + segundos

    def reconstruir_tiempo_a_formato(self, tiempo_segundos: int) -> str: # Método #19
        """
        Introducción
        ------------
            - Método que permite reconstruir un tiempo en formato HH:MM:SS.

        Parámetros
        ----------
            - tiempo_segundos: int, tiempo en segundos, sin valores por defecto.

        Retorna
        -------
            - Tiempo reconstruido en formato HH:MM:SS: str.
        """

        # Cálculo de horas, minutos y segundos
        horas = tiempo_segundos // 3600
        segundos = tiempo_segundos % 60
        minutos = (tiempo_segundos % 3600) // 60

        # Retorno del tiempo con formato
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"