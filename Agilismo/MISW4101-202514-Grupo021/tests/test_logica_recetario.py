# 1st Party Libraries
from src.modelos.Receta import Receta
from src.modelos.Ingrediente import Ingrediente
from tests.faker_recetario import FakerRecetario
from src.logica.LogicaRecetario import LogicaRecetario
from src.modelos.RecetaIngrediente import RecetaIngrediente
from src.modelos.declarative_base import Base, engine, session

# 3rd Party Libraries
import unittest

class TestCaseLogicaRecetario(unittest.TestCase):
    """Unittests que permiten comparar el resultado de los métodos de la clase LogicaRecetario con valores predefinidos en cada prueba."""
    
    def setUp(self) -> None:
        """Configuración de los recursos."""

        # Instanciar Logica Receario
        self.logica = LogicaRecetario()
        
        # Instanciar Faker Recetario
        self.faker = FakerRecetario()
        
        # Eliminación de BD existentes
        Base.metadata.drop_all(engine) 
        
        # Creación de las BD
        Base.metadata.create_all(engine)
        
        # Generación de tiempo aleatorio
        self.tiempo = self.faker.generar_tiempo()
        
        # Generación de tiempos aleatorios
        self.tiempo1 = self.faker.generar_tiempo()
        self.tiempo2 = self.faker.generar_tiempo()
        
        # Generación de número de personas aleatorio
        self.personas = self.faker.generar_personas()
        
        # Generación de número de personas aleatorio
        self.personas1 = self.faker.generar_personas()
        self.personas2 = self.faker.generar_personas()
        
        # Generación de número de calorias aleatorio
        self.calorias = self.faker.generar_calorias()
        
        # Generación de número de calorias aleatorio
        self.calorias1 = self.faker.generar_calorias()
        self.calorias2 = self.faker.generar_calorias()
        
        # Generación de nombre de receta aleatorio
        self.receta = self.faker.generar_receta()
        
        # Generación de nombres de recetas aleatorias
        self.receta1 = self.faker.generar_receta()
        self.receta2 = self.faker.generar_receta()
        
        # Generación de preparación de una receta aleatoria
        self.preparacion = self.faker.generar_preparacion()
        
        # Generación de preparaciones aleatorias
        self.preparacion1 = self.faker.generar_preparacion()
        self.preparacion2 = self.faker.generar_preparacion()

        # Generación de sitio de compra aleatorio
        self.sitioCompra = self.faker.generar_sitio_compra()
        
        # Generación de sitios de compra aleatorios
        self.sitioCompra1 = self.faker.generar_sitio_compra()
        self.sitioCompra2 = self.faker.generar_sitio_compra()
        self.sitioCompra3 = self.faker.generar_sitio_compra()

        # Generación de valor de unidad aleatorio
        self.valorUnidad = self.faker.generar_valor_unidad()
        
        # Generación de valores de unidad aleatorios
        self.valorUnidad1 = self.faker.generar_valor_unidad()
        self.valorUnidad2 = self.faker.generar_valor_unidad()
        self.valorUnidad3 = self.faker.generar_valor_unidad()

        # Generación de unidad de medida aleatoria
        self.unidadMedida = self.faker.generar_unidad_medida()
        
        # Generación de unidades de medida aleatorios
        self.unidadMedida1 = self.faker.generar_unidad_medida()
        self.unidadMedida2 = self.faker.generar_unidad_medida()
        self.unidadMedida3 = self.faker.generar_unidad_medida()

        # Generación de nombre de ingrediente aleatorio
        self.nombreIngrediente = self.faker.generar_nombre_ingrediente()

        # Generación de nombres de ingredientes aleatorios
        self.nombreIngrediente1 = self.faker.generar_nombre_ingrediente()
        self.nombreIngrediente2 = self.faker.generar_nombre_ingrediente()
        self.nombreIngrediente3 = self.faker.generar_nombre_ingrediente()

    def test_validar_crear_receta(self) -> None: # Unittest #1
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_receta con el valor predefinido de la prueba."""

        # Creación de la receta y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_receta(id_receta = None, receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(mensaje_error, "")

    def test_validar_crear_receta_nombre_duplicado(self) -> None: # Unittest #2
       """Unittest que permite comparar el mensaje de error del método validar_crear_editar_receta con el valor predefinido de la prueba."""
       
       # Creación de la receta duplicada
       self.logica.crear_receta(receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)
       
       # Obtención del mensaje de error
       mensaje_error = self.logica.validar_crear_editar_receta(id_receta = None, receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

       # Comparación del mensaje de error con un valor predefinido
       self.assertEqual(mensaje_error, "Ya existe una receta con ese nombre.")

    def test_validar_crear_receta_campo_vacio(self) -> None: #Unittest #3
       """Unittest que permite comparar el mensaje cuando hay presencia de datos vacíos del método validar_crear_editar_receta con el valor predefinido de la prueba."""

       # Creación de la receta con la presencia de valores vacíos y obtención del mensaje
       mensaje_error = self.logica.validar_crear_editar_receta(id_receta = None, receta = self.receta, tiempo = None, personas = self.personas, calorias = '', preparacion = self.preparacion)

       # Comparación del mensaje de presencia de valores vacíos con un valor predefinido
       self.assertEqual(mensaje_error, "Hay datos vacíos.")

    def test_validar_crear_receta_tipo_dato_incorrecto(self) -> None: # Unittest #4
        """Unittest que permite comparar el mensaje cuando se ingresa un tipo de dato tipo string en el parámetro calorías del método validar_crear_editar_receta con el valor predefinido de la prueba."""
       
        # Creación de la receta con el ingreso de un tipo de dato numérico en el parámetro calorias
        mensaje_error = self.logica.validar_crear_editar_receta(id_receta = None, receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = 'aaa', preparacion = self.preparacion)

        # Comparación del mensaje de datos incorrectos con un valor predefinido
        self.assertEqual(mensaje_error, "Hay tipos de datos inválidos.")

    def test_validar_crear_receta_formato_tiempo(self) -> None: # Unittest #5
        """Unittest que permite comparar el mensaje cuando se ingresa un formato incorrecto de tiempo del método validar_crear_editar_receta con el valor predefinido de la prueba."""

        # Creación de la receta con un formato de tiempo ingresado incorrecto y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_receta(id_receta = None, receta = self.receta, tiempo = 'una hora', personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Comparación del mensaje de datos incorrectos con un valor predefinido
        self.assertEqual(mensaje_error, "Hay tipos de datos inválidos.")

    def test_validar_crear_receta_formato_personas(self) -> None: # Unittest #6
        """Unittest que permite comparar el mensaje cuando se ingresa un tipo de dato no númerico sobre el número de personas del método validar_crear_editar_receta con el valor predefinido de la prueba."""
        
        # Creación de la receta con un tipo de dato no númerico sobre el número de personas y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_receta(id_receta = None, receta = self.receta, tiempo = self.tiempo, personas = 'abc', calorias = self.calorias, preparacion = self.preparacion)
        
        # Comparación del mensaje de datos incorrectos con un valor predefinido
        self.assertEqual(mensaje_error, "Hay tipos de datos inválidos.")

    def test_validar_crear_receta_formato_calorias(self) -> None: # Unittest #7
        """Unittest que permite comparar el mensaje cuando se ingresa un tipo de dato no númerico sobre las calorías por porción del método validar_crear_editar_receta con el valor predefinido de la prueba."""

        # Creación de la receta con un tipo de dato no númerico en el parámetro calorías_porcion y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_receta(id_receta = None, receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = 'cinco', preparacion = self.preparacion)

        # Comparación del mensaje de datos incorrectos con un valor predefinido
        self.assertEqual(mensaje_error, "Hay tipos de datos inválidos.")

    def test_crear_receta(self) -> None: # Unittest #8
        """Unittest que permite comparar el mensaje de éxito al crear una receta con todos los campos correctos del método crear_receta con el valor predefinido de la prueba."""
       
        # Creación de la receta y obtención del mensaje
        mensaje_exito = self.logica.crear_receta(receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Comparación del mensaje de creación éxitosa con un valor predefinido
        self.assertEqual(mensaje_exito, "Receta creada exitosamente.")

    def test_dar_recetas_sin_recetas(self) -> None: # Unittest #9
        """Unittest que permite comparar el valor al no haber presencia de recetas del método dar_recetas, con un valor predefinido."""
        
        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine) 
        Base.metadata.create_all(engine)
        
        # Comparación del tamaño del listado vacío, con un valor predefinido
        self.assertEqual(len(self.logica.dar_recetas()), 0)

        # Comparación de la lista vacía, con un valor predefinido
        self.assertEqual(self.logica.dar_recetas(), [])

    def test_dar_recetas(self) -> None: # Unittest #10
        """Unittest que permite identificar el listado de recetas disponibles del método dar_recetas después de su registro, con dos diferentes valores predefinidos."""

        # Creación de dos diferentes recetas
        self.logica.crear_receta(receta = self.receta1, tiempo = self.tiempo1, personas = self.personas1, calorias = self.calorias1, preparacion = self.preparacion1)
        self.logica.crear_receta(receta = self.receta2, tiempo = self.tiempo2, personas = self.personas2, calorias = self.calorias2, preparacion = self.preparacion2)

        # Obtención de las recetas
        recetas = self.logica.dar_recetas()
        
        # Comparación del tamaño de la lista de recetas con un valor predefinido
        self.assertEqual(len(recetas), 2)
        
        # Comparación de la primera y segunda receta, con valores predefinidos
        self.assertEqual(recetas[0]['nombre'], self.receta1)
        self.assertEqual(recetas[1]['nombre'], self.receta2)

    def test_dar_ingredientesreceta_sin_receta(self) -> None: # Unittest #11
        """Unittest que permite comparar si el resultado vacío del método dar_ingredientes_receta, y el tamaño de su resultado vacío es equivalente a los valores predefinidos de la prueba."""
        
        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine) 
        Base.metadata.create_all(engine)

        # Comparación de dos formas para evaluar si la lista se encuentra vacía
        self.assertEqual(len(self.logica.dar_ingredientes_receta(id_receta = 999)), 0)
        self.assertEqual(self.logica.dar_ingredientes_receta(id_receta = 999), [])

    def test_dar_ingredientesreceta_sin_ingredientes(self) -> None: # Unittest #12
        """Unittest que permite comparar si el resultado de un registro de una receta sin ingredientes del método dar_ingredientes_receta, y el tamaño de su resultado vacío es equivalente a los valores predefinidos de la prueba."""
        
        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación de la receta sin ingredientes
        self.logica.crear_receta(receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Comparación de dos formas para evaluar si la lista de ingredientes se encuentra vacía
        self.assertEqual(len(self.logica.dar_ingredientes_receta(id_receta = 1)), 0)
        self.assertEqual(self.logica.dar_ingredientes_receta(id_receta = 1), [])

    def test_dar_ingredientesreceta(self) -> None: # Unittest #13
        """Unittest que permite comparar si después de registrar una receta, con sus ingredientes, se puede obtener el listado del método dar_ingredientes_receta, el tamaño del listado y si ambos resultados son equivalentes a los valores predefinidos de la prueba."""
        
        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación de la receta
        self.logica.crear_receta(receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente1, unidad_medida = self.unidadMedida1, valor_unidad = self.valorUnidad1, sitio_compra = self.sitioCompra1)
        ingrediente2 = Ingrediente(nombre = self.nombreIngrediente2, unidad_medida = self.unidadMedida2, valor_unidad = self.valorUnidad2, sitio_compra = self.sitioCompra2)

        # Asociación de ingredientes en la receta Ajiaco y colocación de la cantidad
        recetaIngrediente1 = RecetaIngrediente(id_receta = 1, id_ingrediente = 1, cantidad_ingrediente = 1)
        recetaIngrediente2 = RecetaIngrediente(id_receta = 1, id_ingrediente = 2, cantidad_ingrediente = 2)
        
        # Agregar ingredientes a la tabla Ingrediente
        session.add(ingrediente1)
        session.add(ingrediente2)

        # Agregar ingredientes a la tabla Receta Ingrediente
        session.add(recetaIngrediente1)
        session.add(recetaIngrediente2)
        
        # Aplicar cambios
        session.commit()

        # Comparación de dos formas para corroborar que se encuentran dos ingredientes en la receta
        self.assertEqual(len(self.logica.dar_ingredientes_receta(0)), 2)
        self.assertEqual(self.logica.dar_ingredientes_receta(0), [{'receta': self.receta, 'ingrediente': self.nombreIngrediente1, 'unidad': self.unidadMedida1, 'cantidad': 1}, 
                                                                  {'receta': self.receta, 'ingrediente': self.nombreIngrediente2, 'unidad': self.unidadMedida2, 'cantidad': 2}])

    def test_validar_crear_editar_ingrediente(self) -> None: # Unittest #14
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingrediente con el valor predefinido de la prueba."""

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingrediente(nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra, esCreacion = True)

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(mensaje_error, "")

    def test_validar_crear_editar_ingrediente_nombre_duplicado(self) -> None: # Unittest #15
        """Unittest que permite comparar el mensaje de error del método validar_crear_editar_ingrediente cuando se ingresa un nombre duplicado, con el valor predefinido de la prueba."""

        # Creación del ingrediente duplicado
        self.logica.crear_ingrediente(nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra)

        # Validación del ingrediente duplicado y obtención del mensaje de error
        mensaje_error = self.logica.validar_crear_editar_ingrediente(nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra, esCreacion = True)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "Ya existe un ingrediente con ese nombre.")

    def test_validar_crear_editar_ingrediente_campo_vacio(self) -> None: # Unittest #16
        """Unittest que permite comparar el mensaje cuando hay presencia de datos vacíos del método validar_crear_editar_ingrediente con el valor predefinido de la prueba."""
        
        # Validación del ingrediente con la presencia de valores vacíos y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingrediente(nombre = self.nombreIngrediente, unidad = None, valor = self.valorUnidad, sitioCompra = self.sitioCompra, esCreacion = True)

        # Comparación del mensaje de presencia de valores vacíos con un valor predefinido
        self.assertEqual(mensaje_error, "Hay datos vacíos.")
    
    def test_validar_crear_editar_ingrediente_tipo_dato_incorrecto(self) -> None: # Unittest #17
        """Unittest que permite comparar el mensaje cuando se ingresa un tipo de dato no string en el parámetro nombre del método validar_crear_editar_ingrediente con el valor predefinido de la prueba."""
       
        # Validación del ingrediente con el ingreso de un tipo de dato numérico en el parámetro nombre
        mensaje_error = self.logica.validar_crear_editar_ingrediente(nombre = self.nombreIngrediente, unidad = 10, valor = self.valorUnidad, sitioCompra = self.sitioCompra, esCreacion = True)

        # Comparación del mensaje de datos incorrectos con un valor predefinido
        self.assertEqual(mensaje_error, "Hay tipos de datos inválidos.")

    def test_validar_crear_editar_ingrediente_formato_valor(self) -> None: # Unittest #18
        """Unittest que permite comparar el mensaje cuando se ingresa un tipo de dato no numérico en el parámetro valor del método validar_crear_editar_ingrediente con el valor predefinido de la prueba."""

        # Validación del ingrediente con un tipo de dato no númerico en el parámetro valor
        mensaje_error = self.logica.validar_crear_editar_ingrediente(nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = 'quince mil', sitioCompra = self.sitioCompra, esCreacion = True)

        # Comparación del mensaje de datos incorrectos con un valor predefinido
        self.assertEqual(mensaje_error, "Hay tipos de datos inválidos.")

    def test_crear_ingrediente(self) -> None: # Unittest #19
        """Unittest que permite comparar el mensaje de éxito al crear un ingrediente con todos los campos correctos del método crear_ingrediente con el valor predefinido de la prueba."""
        
        # Creación del ingrediente y obtención del mensaje
        mensaje_exito = self.logica.crear_ingrediente(nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra)

        # Comparación del mensaje de creación éxitosa con un valor predefinido
        self.assertEqual(mensaje_exito, "Ingrediente creado exitosamente.")

    def test_dar_ingredientes_sin_ingredientes(self) -> None: # Unittest #20
        """Unittest que permite comparar el resultado obtenido del método dar_ingredientes, sin ingredientes disponibles, con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Comparación del listado vacío con un mensaje predefinido
        self.assertEqual(self.logica.dar_ingredientes(), [])
    
    def test_dar_ingredientes(self) -> None: # Unittest #21
        """Unittest que permite comparar el resultado obtenido del método dar_ingredientes, teniendo ingredientes disponibles, con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente1, unidad_medida = self.unidadMedida1, valor_unidad = self.valorUnidad1, sitio_compra = self.sitioCompra1)
        ingrediente2 = Ingrediente(nombre = self.nombreIngrediente2, unidad_medida = self.unidadMedida2, valor_unidad = self.valorUnidad2, sitio_compra = self.sitioCompra2)

        # Agregar ingredientes a la tabla Ingrediente
        session.add(ingrediente1)
        session.add(ingrediente2)

        # Aplicar cambios
        session.commit()

        # Comparación de dos formas para corroborar que se encuentran dos ingredientes en el listado
        self.assertEqual(len(self.logica.dar_ingredientes()), 2)
        self.assertEqual(self.logica.dar_ingredientes(), [{'id': 1, 'nombre': self.nombreIngrediente1, 'unidad': self.unidadMedida1, 'valor': float(self.valorUnidad1), 'sitioCompra': self.sitioCompra1}, 
                                                          {'id': 2, 'nombre': self.nombreIngrediente2, 'unidad': self.unidadMedida2, 'valor': float(self.valorUnidad2), 'sitioCompra': self.sitioCompra2}])

    def test_validar_crear_editar_ingReceta(self) -> None: # Unittest #22
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingReceta con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

        # Agregar receta e ingrediente a la BD
        session.add(receta1)
        session.add(ingrediente1)

        # Aplicar cambios
        session.commit()

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingReceta(receta = receta1.to_dict(), ingrediente = ingrediente1.to_dict(), cantidad = "1")

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(mensaje_error, "")

    def test_validar_crear_editar_ingReceta_receta_sin_id(self) -> None: # Unittest #23
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingReceta cuando la receta no tiene id."""

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingReceta(receta = {}, ingrediente = {}, cantidad = "1")

        # Comparación del mensaje de error
        self.assertEqual(mensaje_error, "La receta no tiene id.")

    def test_validar_crear_editar_ingReceta_ingrediente_sin_id(self) -> None: # Unittest #24
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingReceta cuando el ingrediente no tiene id."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Agregar receta a la BD
        session.add(receta1)

        # Aplicar cambios
        session.commit()

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingReceta(receta = receta1.to_dict(), ingrediente = {}, cantidad = "1")

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "El ingrediente no tiene id.")  

    def test_validar_crear_editar_ingReceta_formato_cantidad(self) -> None: # Unittest #25
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingReceta cuando la cantidad no tiene un formato válido."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

        # Agregar receta e ingrediente a la BD
        session.add(receta1)
        session.add(ingrediente1)

        # Aplicar cambios
        session.commit()

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingReceta(receta = receta1.to_dict(), ingrediente = ingrediente1.to_dict(), cantidad = "uno")

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "Hay datos inválidos.")

    def test_validar_crear_editar_ingReceta_cantidad_positiva(self) -> None: # Unittest #26
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingReceta cuando la cantidad es positiva."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

        # Agregar receta e ingrediente a la BD
        session.add(receta1)
        session.add(ingrediente1)

        # Aplicar cambios
        session.commit()

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingReceta(receta = receta1.to_dict(), ingrediente = ingrediente1.to_dict(), cantidad = "-1")

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "Hay datos inválidos.")

    def test_validar_crear_editar_ingReceta_receta_no_existe(self) -> None: # Unittest #27
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingReceta cuando la receta no existe en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

        # Agregar ingrediente a la BD
        session.add(ingrediente1)

        # Aplicar cambios
        session.commit()

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingReceta(receta = {'id': 999}, ingrediente = ingrediente1.to_dict(), cantidad = "1")

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "La receta no existe.")

    def test_validar_crear_editar_ingReceta_ingrediente_no_existe(self) -> None: # Unittest #28
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingReceta cuando el ingrediente no existe en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Agregar receta a la BD
        session.add(receta1)

        # Aplicar cambios
        session.commit()

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingReceta(receta = receta1.to_dict(), ingrediente = {'id': 999}, cantidad = "1")

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "El ingrediente no existe.")

    def test_agregar_ingrediente_receta(self) -> None: # Unittest #29
        """Unittest que permite comparar el mensaje de éxito al agregar un ingrediente a una receta del método agregar_ingrediente_receta con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

        # Agregar receta e ingrediente a la BD
        session.add(receta1)
        session.add(ingrediente1)

        # Aplicar cambios
        session.commit()

        # Agregar ingrediente a la receta y obtención del mensaje
        mensaje_exito = self.logica.agregar_ingrediente_receta(receta = receta1.to_dict(), ingrediente = ingrediente1.to_dict(), cantidad = "1")

        # Comparación del mensaje de creación éxitosa con un valor predefinido
        self.assertEqual(mensaje_exito, "Ingrediente agregado a la receta exitosamente.")

    def test_eliminar_ingrediente_id_no_existe(self) -> None: # Unittest #30
        """Unittest que permite comparar el mensaje de error al eliminar un ingrediente cuando el id del ingrediente no existe en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

        # Agregar receta e ingrediente a la BD
        session.add(ingrediente1)

        # Aplicar cambios
        session.commit()

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente(id_ingrediente = 999), "El ingrediente no existe.")

    def test_eliminar_ingrediente_no_hay_ingredientes(self) -> None: # Unittest #31
        """Unittest que permite comparar el mensaje de error al eliminar un ingrediente cuando no hay ingredientes en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente(id_ingrediente = 0), "No hay ingredientes para eliminar.")

    def test_eliminar_ingrediente_usado_en_receta(self) -> None: # Unittest #32
        """Unittest que permite comparar el mensaje de error al eliminar un ingrediente cuando está siendo usado en una receta."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)
        recetaIngrediente1 = RecetaIngrediente(id_receta = 1, id_ingrediente = 1, cantidad_ingrediente = 1)

        # Agregar receta, ingrediente a la BD y receta ingrediente en receta         
        session.add(receta1)
        session.add(ingrediente1)
        session.add(recetaIngrediente1)

        # Aplicar cambios
        session.commit()

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente(id_ingrediente = 0), "El ingrediente no puede ser eliminado porque está siendo utilizado en una receta.")

    def test_eliminar_ingrediente(self) -> None: # Unittest #33
        """Unittest que permite comparar el mensaje de éxito al eliminar un ingrediente del método eliminar_ingrediente con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

        # Agregar receta e ingrediente a la BD
        session.add(ingrediente1)

        # Aplicar cambios
        session.commit()

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente(id_ingrediente = 0), "Ingrediente eliminado exitosamente.")

        # Comparación del tamaño del listado vacío, con un valor predefinido
        self.assertEqual(len(self.logica.dar_ingredientes()), 0)

    def test_eliminar_ingrediente_varios_ingredientes(self) -> None: # Unittest #34
        """Unittest que permite comparar el mensaje de éxito al eliminar un ingrediente del método eliminar_ingrediente con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente1, unidad_medida = self.unidadMedida1, valor_unidad = self.valorUnidad1, sitio_compra = self.sitioCompra1)
        ingrediente2 = Ingrediente(nombre = self.nombreIngrediente2, unidad_medida = self.unidadMedida2, valor_unidad = self.valorUnidad2, sitio_compra = self.sitioCompra2)
        ingrediente3 = Ingrediente(nombre = self.nombreIngrediente3, unidad_medida = self.unidadMedida3, valor_unidad = self.valorUnidad3, sitio_compra = self.sitioCompra3)

        # Agregar receta e ingrediente a la BD
        session.add(ingrediente1)
        session.add(ingrediente2)
        session.add(ingrediente3)

        # Aplicar cambios
        session.commit()

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente(id_ingrediente = 0), "Ingrediente eliminado exitosamente.")

        # Comparación del tamaño del listado vacío, con un valor predefinido
        self.assertEqual(len(self.logica.dar_ingredientes()), 2)

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente(id_ingrediente = 1), "Ingrediente eliminado exitosamente.")

        # Comparación del tamaño del listado vacío, con un valor predefinido
        self.assertEqual(len(self.logica.dar_ingredientes()), 1)

         # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente(id_ingrediente = 0), "Ingrediente eliminado exitosamente.")

        # Comparación del tamaño del listado vacío, con un valor predefinido
        self.assertEqual(len(self.logica.dar_ingredientes()), 0)

    def test_eliminar_receta_id_no_existe(self) -> None: # Unittest #35
        """Unittest que permite comparar el mensaje de error al eliminar una receta cuando el id de la receta no existe en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación de una receta
        receta = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)
        session.add(receta)
        session.commit()

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.eliminar_receta(id_receta = 999), "La receta no existe.")

    def test_eliminar_receta_no_hay_recetas(self) -> None: # Unittest #36
        """Unittest que permite comparar el mensaje de error al eliminar una receta cuando no hay recetas en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.eliminar_receta(id_receta = 0), "No hay recetas para eliminar.")

    def test_eliminar_receta(self) -> None: # Unittest #37
        """Unittest que permite comparar el mensaje de éxito al eliminar una receta del método eliminar_receta con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación de una receta
        receta = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)
        session.add(receta)
        session.commit()

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(self.logica.eliminar_receta(id_receta = 0), "Receta eliminada exitosamente.")

        # Comparación del tamaño del listado vacío, con un valor predefinido
        self.assertEqual(len(self.logica.dar_recetas()), 0)

    def test_editar_ingrediente_receta_idrecetaingrediente_no_existe(self) -> None: # Unittest #38
        """Unittest que permite comparar el mensaje de error al editar un ingrediente en una receta cuando el id de la tabla RecetaIngrediente no existe en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.editar_ingrediente_receta(id_ingrediente_receta = 999, receta = {}, ingrediente = {}, cantidad = "2"), "El ingrediente en la receta no existe.")

    def test_editar_ingrediente_receta(self) -> None: # Unittest #39
        """Unittest que permite comparar el mensaje de éxito al editar un ingrediente en una receta del método editar_ingrediente_receta con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)
        recetaIngrediente1 = RecetaIngrediente(id_receta = 1, id_ingrediente = 1, cantidad_ingrediente = 1)

        # Agregar receta, ingrediente a la BD y receta ingrediente en receta         
        session.add(receta1)
        session.add(ingrediente1)
        session.add(recetaIngrediente1)

        # Aplicar cambios
        session.commit()

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(self.logica.editar_ingrediente_receta(id_ingrediente_receta = 0, receta = receta1.to_dict(), ingrediente = ingrediente1.to_dict(), cantidad = "2"), "Ingrediente en la receta editado exitosamente.")

        # Comparación de la cantidad editada del ingrediente en la receta
        self.assertEqual(self.logica.dar_ingredientes_receta(id_receta = 0), [{'receta': self.receta, 'ingrediente': self.nombreIngrediente, 'unidad': self.unidadMedida, 'cantidad': 2}])

    def test_editar_ingrediente_sin_ingredientes(self) -> None: # Unittest #40
        """Unittest que permite comparar el mensaje de error al intentar editar un ingrediente con un listado vacío, a partir del uso del método editar_ingrediente con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Completar la edición de ingredientes, cuando el listado se encuentra vacío y obtención del mensaje de error
        mensaje_error = self.logica.editar_ingrediente(id_ingrediente = 1, nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "No hay ingredientes para editar.")

    def test_editar_ingrediente_en_receta(self) -> None: # Unittest #41
        """Unittest que permite comparar el mensaje de error al intentar editar un ingrediente que se encuentra en una receta, a partir del uso del método editar_ingrediente con el valor predefinido de la prueba. """

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)
        recetaIngrediente1 = RecetaIngrediente(id_receta = 1, id_ingrediente = 1, cantidad_ingrediente = 1)

        # Agregar receta, ingrediente a la BD y receta ingrediente en receta        
        session.add(receta1)
        session.add(ingrediente1)
        session.add(recetaIngrediente1)

        # Aplicar cambios
        session.commit()

        # Edición de Ingrediente y comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.editar_ingrediente(id_ingrediente = 0, nombre = 'Yuca', unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra), "El ingrediente se encuentra agregado en una receta.")

    def test_editar_ingrediente_id_no_existe(self) -> None: # Unittest #42
        """Unittest que permite comparar el mensaje de error al intentar editar un ingrediente cuyo id no existe, a partir del uso del método editar_ingrediente con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación de un ingrediente
        ingrediente = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)
        
        # Agregar Ingrediente en BD
        session.add(ingrediente)

        # Aplicación de Cambios
        session.commit()

        # Edición de Ingrediente y comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.editar_ingrediente(id_ingrediente = 999, nombre = 'Yuca', unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra), "El ingrediente no existe.")

    def test_editar_ingrediente(self) -> None: # Unittest #43
       """Unittest que permite comparar el resultado obtenido después de editar un ingrediente, con la lectura de un ingrediente predefinido de la prueba."""

       # Eliminación de datos y creación de la BD
       Base.metadata.drop_all(engine)
       Base.metadata.create_all(engine)

       # Instanciar clase y preparación del primer ingrediente y segundo ingrediente
       ingrediente = Ingrediente(nombre = self.nombreIngrediente, unidad_medida = self.unidadMedida, valor_unidad = self.valorUnidad, sitio_compra = self.sitioCompra)

       # Agregar receta, ingrediente a la BD y receta ingrediente en receta
       session.add(ingrediente)

       # Aplicar cambios
       session.commit()

       # Comparación del mensaje de éxito con un valor predefinido
       self.assertEqual(self.logica.editar_ingrediente(id_ingrediente = 0, nombre = 'Yuca', unidad = 'Libra', valor = self.valorUnidad, sitioCompra = self.sitioCompra), "Ingrediente actualizado exitosamente.")

    def test_validar_crear_editar_ingrediente_no_valida_nombre_editanto(self) -> None: # Unittest #44
        """Unittest que permite comparar el mensaje de éxito del método validar_crear_editar_ingrediente cuando se está editando un ingrediente y no valida el nombre, con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación del ingrediente
        self.logica.crear_ingrediente(nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra)

        # Validación del ingrediente y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_ingrediente(nombre = self.nombreIngrediente, unidad = self.unidadMedida, valor = self.valorUnidad, sitioCompra = self.sitioCompra, esCreacion = False)

        # Comparación del mensaje de éxito con un valor predefinido
        self.assertEqual(mensaje_error, "")

    def test_validar_crear_editar_receta_id_no_existe(self) -> None: # Unittest #45
        """Unittest que permite comparar el mensaje de error al intentar editar una receta cuyo id no existe, a partir del uso del método validar_crear_editar_receta con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Validación de la receta y obtención del mensaje
        mensaje_error = self.logica.validar_crear_editar_receta(id_receta = 999, receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "La receta no existe.")

    def test_validar_crear_editar_receta_nombre_duplicado_editando(self) -> None: # Unittest #46
        """Unittest que permite comparar el mensaje de error del método validar_crear_editar_receta cuando se ingresa un nombre duplicado al editar, con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación de dos recetas
        self.logica.crear_receta(receta = self.receta1, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)
        self.logica.crear_receta(receta = self.receta2, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Validación del ingrediente duplicado y obtención del mensaje de error
        mensaje_error = self.logica.validar_crear_editar_receta(id_receta = 0, receta = self.receta2, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(mensaje_error, "Ya existe una receta con ese nombre.")

    def test_editar_receta(self) -> None: # Unittest #47
         """Unittest que permite comparar el resultado obtenido después de editar una receta, con la lectura de una receta predefinida de la prueba."""
    
         # Eliminación de datos y creación de la BD
         Base.metadata.drop_all(engine)
         Base.metadata.create_all(engine)
    
         # Creación de una receta
         self.logica.crear_receta(receta = self.receta1, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)
    
         # Edición de la receta y comparación del mensaje de éxito con un valor predefinido
         self.assertEqual(self.logica.editar_receta(id_receta = 0, receta = 'Sancocho', tiempo = '90:00:00', personas = '6', calorias = '600', preparacion = 'Cocinar todo junto por 2 horas.'), "Receta actualizada exitosamente.")
    
         # Comparación del resultado obtenido después de editar una receta, con la lectura de una receta predefinida de la prueba
         self.assertEqual(self.logica.dar_recetas(), [{'id': 1, 'nombre': 'Sancocho', 'tiempo': '90:00:00', 'personas': 6, 'calorias': 600, 'preparacion': 'Cocinar todo junto por 2 horas.'}])

    def test_dar_receta(self) -> None: # Unittest #48
        """Unittest que permite comparar el resultado obtenido del método listar_receta con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Crear una receta
        self.logica.crear_receta(receta = self.receta, tiempo = self.tiempo, personas = self.personas, calorias = self.calorias, preparacion = self.preparacion)

        # Comparación del listado de recetas con un valor predefinido
        self.assertEqual(self.logica.dar_receta(id_receta = 0), {'id': 1, 'nombre': self.receta, 'tiempo': self.tiempo, 'personas': int(self.personas), 'calorias': float(self.calorias), 'preparacion': self.preparacion})

    def test_eliminar_ingrediente_receta_sin_ingredientes(self) -> None: # Unittest #49
        """Unittest que permite comparar el mensaje generado por el método eliminar_ingrediente receta al intentar borrar ingredientes de una receta sin ingredientes, con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Agregar receta a la BD
        session.add(receta1)

        # Aplicar cambios
        session.commit()
       
        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente_receta(id_ingrediente_receta = 1, receta = receta1.to_dict()), "No hay ingredientes en la receta para eliminar.")

    def test_eliminar_ingrediente(self) -> None: # Unittest #50
        """Unittest que realiza la eliminación del ingrediente en una receta y compara el listado disponible, con el listado predefinido en la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente1, unidad_medida = self.unidadMedida1, valor_unidad = self.valorUnidad1, sitio_compra = self.sitioCompra1)
        ingrediente2 = Ingrediente(nombre = self.nombreIngrediente2, unidad_medida = self.unidadMedida2, valor_unidad = self.valorUnidad2, sitio_compra = self.sitioCompra2)
        
        # Incorporación del ingrediente # 1 a la receta
        recetaIngrediente1 = RecetaIngrediente(id_receta = 1, id_ingrediente = 1, cantidad_ingrediente = 1)
        recetaIngrediente2 = RecetaIngrediente(id_receta = 1, id_ingrediente = 2, cantidad_ingrediente = 2)

        # Agregar receta, ingrediente a la BD y receta ingrediente en receta         
        session.add(receta1)
        session.add(ingrediente1)
        session.add(ingrediente2)
        session.add(recetaIngrediente1)
        session.add(recetaIngrediente2)

        # Aplicar cambios
        session.commit()

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.eliminar_ingrediente_receta(id_ingrediente_receta = 1, receta = receta1.to_dict()), "Ingrediente de receta eliminado exitosamente.")

    def test_preparar_receta_no_hay_recetas(self) -> None: # Unittest #51
        """Unittest que permite comparar el mensaje de error al intentar preparar una receta cuando no hay recetas en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.dar_preparacion(id_receta = 0, personas = 2), "No hay recetas para preparar.")

    def test_preparar_receta_id_no_existe(self) -> None: # Unittest #52
        """Unittest que permite comparar el mensaje de error al intentar preparar una receta cuyo id no existe en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Creación de una receta
        receta = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)
        session.add(receta)
        session.commit()

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.dar_preparacion(id_receta = 999, personas = 2), "La receta no existe.")

    def test_preparar_receta_formato_personas(self) -> None: # Unittest #53
        """Unittest que permite comparar el mensaje de error al intentar preparar una receta cuando el número de personas no tiene un formato válido."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = self.personas, calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Agregar receta a la BD
        session.add(receta1)

        # Aplicar cambios
        session.commit()

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.dar_preparacion(id_receta = 0, personas = 'dos'), "Hay datos inválidos.")

    def test_preparar_receta_sin_ingredientes_cantidad_personas_menor(self) -> None: # Unittest #54
        """Unittest que permite comparar el mensaje de error al intentar preparar una receta cuando no hay ingredientes en la BD."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        numero_personas_mayor = int(self.personas) + 3

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = str(numero_personas_mayor), calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Agregar receta a la BD
        session.add(receta1)

        # Aplicar cambios
        session.commit()

        # Separación tiempo por partes
        tiempo_partes = self.tiempo.split(':')
        
        # Obtención de las horas, minutos y segundos
        horas = int(tiempo_partes[0])
        minutos = int(tiempo_partes[1])
        segundos = int(tiempo_partes[2])

        # Número de personas
        numero_personas_menor = numero_personas_mayor - 2

        # Calculo del Factor de Ajuste
        factor_ajuste = (numero_personas_mayor - numero_personas_menor) / (2 * numero_personas_mayor)

        # Ajustes en tiempo y factor de ajuste
        tiempo_total_segundos = horas * 3600 + minutos * 60 + segundos
        
        # Tiempo ajustado segundos
        tiempo_ajustado_segundos = tiempo_total_segundos - (factor_ajuste * tiempo_total_segundos)
        tiempo_ajustado_segundos = max(0, int(tiempo_ajustado_segundos))

        # Segundos, horas y minutos ajustados
        segundos_ajustados = tiempo_ajustado_segundos % 60
        horas_ajustadas = tiempo_ajustado_segundos // 3600
        minutos_ajustados = (tiempo_ajustado_segundos % 3600) // 60

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.dar_preparacion(id_receta = 0, personas = numero_personas_menor), 
                         {'receta': self.receta,
                          'personas': numero_personas_menor, 
                          'calorias': round(int(self.calorias) * numero_personas_menor / numero_personas_mayor, 0),
                          'costo': 0, 
                          'tiempo_preparacion': f"{horas_ajustadas:02d}:{minutos_ajustados:02d}:{segundos_ajustados:02d}",
                          'datos_ingredientes': []})
        
    def test_preparar_receta_con_ingredientes_cantidad_personas_menor(self) -> None: # Unittest #55
        """Unittest que permite comparar el mensaje generado por el método dar_preparacion al preparar una receta con ingredientes, con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        numero_personas_mayor = int(self.personas) + 3

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = str(numero_personas_mayor), calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente1, unidad_medida = self.unidadMedida1, valor_unidad = self.valorUnidad1, sitio_compra = self.sitioCompra1)
        ingrediente2 = Ingrediente(nombre = self.nombreIngrediente2, unidad_medida = self.unidadMedida2, valor_unidad = self.valorUnidad2, sitio_compra = self.sitioCompra2)
        
        # Incorporación del ingrediente # 1 a la receta
        recetaIngrediente1 = RecetaIngrediente(id_receta = 1, id_ingrediente = 1, cantidad_ingrediente = 1)
        recetaIngrediente2 = RecetaIngrediente(id_receta = 1, id_ingrediente = 2, cantidad_ingrediente = 2)

        # Agregar receta, ingrediente a la BD y receta ingrediente en receta         
        session.add(receta1)
        session.add(ingrediente1)
        session.add(ingrediente2)
        session.add(recetaIngrediente1)
        session.add(recetaIngrediente2)

        # Aplicar cambios
        session.commit()

        # Separación tiempo por partes
        tiempo_partes = self.tiempo.split(':')
        
        # Obtención de las horas, minutos y segundos
        horas = int(tiempo_partes[0])
        minutos = int(tiempo_partes[1])
        segundos = int(tiempo_partes[2])

        # Número de personas
        numero_personas_menor = numero_personas_mayor - 2

        # Calculo del Factor de Ajuste
        factor_ajuste = (numero_personas_mayor - numero_personas_menor) / (2 * numero_personas_mayor)

        # Ajustes en tiempo y factor de ajuste
        tiempo_total_segundos = horas * 3600 + minutos * 60 + segundos
        
        # Tiempo ajustado segundos
        tiempo_ajustado_segundos = tiempo_total_segundos - (factor_ajuste * tiempo_total_segundos)
        tiempo_ajustado_segundos = max(0, int(tiempo_ajustado_segundos))

        # Segundos, horas y minutos ajustados
        segundos_ajustados = tiempo_ajustado_segundos % 60
        horas_ajustadas = tiempo_ajustado_segundos // 3600
        minutos_ajustados = (tiempo_ajustado_segundos % 3600) // 60

        # Costo proporcional 
        costo_base= round((1 * float(self.valorUnidad1)) + (2 * float(self.valorUnidad2)), 2)
        costo_proporcional = round(costo_base * numero_personas_menor / numero_personas_mayor, 0)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.dar_preparacion(0, numero_personas_menor), 
                         {'receta': self.receta,
                          'personas': numero_personas_menor,
                          'calorias': round(int(self.calorias) * numero_personas_menor / numero_personas_mayor, 0),
                          'costo': costo_proporcional,
                          'tiempo_preparacion': f"{horas_ajustadas:02d}:{minutos_ajustados:02d}:{segundos_ajustados:02d}",
                          'datos_ingredientes': [{**ingrediente1.to_dict(), 'cantidad': 1}, {**ingrediente2.to_dict(), 'cantidad': 2}],})

    def test_preparar_receta_con_ingredientes_cantidad_personas_mayor(self) -> None: # Unittest #56
        """Unittest que permite comparar el mensaje generado por el método dar_preparacion al preparar una receta con ingredientes, con el valor predefinido de la prueba."""

        # Eliminación de datos y creación de la BD
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        numero_personas_menor = int(self.personas) + 1

        # Instanciar clase receta
        receta1 = Receta(nombre = self.receta, tiempo_preparacion = self.tiempo, numero_personas = str(numero_personas_menor), calorias_porcion = self.calorias, instrucciones_preparacion = self.preparacion)

        # Instanciar clase y preparación de ingredientes
        ingrediente1 = Ingrediente(nombre = self.nombreIngrediente1, unidad_medida = self.unidadMedida1, valor_unidad = self.valorUnidad1, sitio_compra = self.sitioCompra1)
        ingrediente2 = Ingrediente(nombre = self.nombreIngrediente2, unidad_medida = self.unidadMedida2, valor_unidad = self.valorUnidad2, sitio_compra = self.sitioCompra2)
        
        # Incorporación del ingrediente # 1 a la receta
        recetaIngrediente1 = RecetaIngrediente(id_receta = 1, id_ingrediente = 1, cantidad_ingrediente = 1)
        recetaIngrediente2 = RecetaIngrediente(id_receta = 1, id_ingrediente = 2, cantidad_ingrediente = 2)

        # Agregar receta, ingrediente a la BD y receta ingrediente en receta         
        session.add(receta1)
        session.add(ingrediente1)
        session.add(ingrediente2)
        session.add(recetaIngrediente1)
        session.add(recetaIngrediente2)

        # Aplicar cambios
        session.commit()

        # Separación tiempo por partes
        tiempo_partes = self.tiempo.split(':')
        
        # Obtención de las horas, minutos y segundos
        horas = int(tiempo_partes[0])
        minutos = int(tiempo_partes[1])
        segundos = int(tiempo_partes[2])

        # Cálculo del tiempo total en segundos
        tiempo_total_segundos = horas * 3600 + minutos * 60 + segundos

        # Número de personas
        numero_personas_mayor = numero_personas_menor + 3

        # Calculo del Factor de Ajuste
        personas_adicionales = numero_personas_mayor - numero_personas_menor
        grupos_adicionales = personas_adicionales // numero_personas_menor
        tiempo_adicional_por_grupo = (2 * tiempo_total_segundos) / 100
        tiempo_adicional_total = grupos_adicionales * tiempo_adicional_por_grupo

        # Tiempo ajustado segundos
        tiempo_ajustado_segundos = tiempo_total_segundos + tiempo_adicional_total
        tiempo_ajustado_segundos = max(0, int(tiempo_ajustado_segundos))

        # Segundos, horas y minutos ajustados
        segundos_ajustados = tiempo_ajustado_segundos % 60
        horas_ajustadas = tiempo_ajustado_segundos // 3600
        minutos_ajustados = (tiempo_ajustado_segundos % 3600) // 60

        # Costo proporcional
        costo_base= round((1 * float(self.valorUnidad1)) + (2 * float(self.valorUnidad2)), 2)
        costo_proporcional = round(costo_base * numero_personas_mayor / numero_personas_menor, 0)

        # Comparación del mensaje de error con un valor predefinido
        self.assertEqual(self.logica.dar_preparacion(0, numero_personas_mayor), {'receta': self.receta,
                                                                                 'personas': numero_personas_mayor,
                                                                                 'calorias': round(int(self.calorias) * numero_personas_mayor / numero_personas_menor, 0),
                                                                                 'costo': costo_proporcional,
                                                                                 'tiempo_preparacion': f"{horas_ajustadas:02d}:{minutos_ajustados:02d}:{segundos_ajustados:02d}",
                                                                                 'datos_ingredientes': [{**ingrediente1.to_dict(), 'cantidad': 1}, {**ingrediente2.to_dict(), 'cantidad': 2}],})

    def tearDown(self) -> None:
        """Limpieza del entorno."""

        # Deshabilitacion de la instancia Logica
        self.logica = None

if __name__ == '__main__':
    unittest.main(exit = False)
