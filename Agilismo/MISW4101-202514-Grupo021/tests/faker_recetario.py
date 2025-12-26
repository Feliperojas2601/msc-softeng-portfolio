# 3rd Party Libraries
import random
from faker import Faker

class FakerRecetario:
    """Clase para generar datos falsos (recetas e ingredientes) usando Faker."""

    def __init__(self, locale: str = "es_CO") -> None: # Constructor
        """Constructor de la clase FakerRecetario."""

        # Instanciar Faker
        self.fake = Faker(locale)

    def generar_receta(self) -> str: # Método #1
        """Método que permite la generación de nombres de recetas aleatorios."""

        # Retorno de nombres aleatorios de receta
        return random.choice(["Ajiaco", "Consome", "Pure", "Sancocho", "Bandeja Paisa", "Tamales"]) + " " + random.choice(["Especial", "Casero", "Tradicional", "Criollo"])

    def generar_tiempo(self) -> str: # Método #2
        """Método que permite la generación de tiempos de preparación con valores aleatorios."""
        
        # Creación de horas, minutos y segundos con valores aleatorios
        horas = random.randint(0, 5)
        minutos = random.randint(0, 59)
        segundos = random.randint(0, 59)

        # Retorno de tiempos de preaparación aleatorios
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    def generar_personas(self) -> str: # Método #3
        """Método que permite la generación de un número de personas aleatorio."""

        # Retorno de un número aleatorio de personas
        return str(random.randint(1, 10))

    def generar_calorias(self) -> str: # Método #4
        """Método que permite la generación de un nnúmero de calorias aleatorio."""
        
        # Retorno de un número aleatorio de calorías
        return str(random.randint(100, 1000))

    def generar_preparacion(self) -> str: # Método #5
        """Método que permite la generación de una preparación de una receta aleatorio."""

        # Retorno de una preparación aleatoria de una receta
        return self.fake.sentence(nb_words = 8)

    def generar_receta_dict(self) -> dict: # Método #6
        """Método que permite generar una receta e información adicional de forma aleatoria."""

        # Retorno de una receta y su información de forma aleatoria
        return {"receta": self.generar_receta_nombre(),
                "tiempo": self.generar_tiempo(),
                "personas": self.generar_personas(),
                "calorias": self.generar_calorias(),
                "preparacion": self.generar_preparacion(),}

    def generar_nombre_ingrediente(self) -> str: # Método #7
        """Método que permite generar el nombre de un ingrediente aleatorio."""

        # Retorno de un nombre de ingrediente aleatorio
        return random.choice(["Pollo", "Papa", "Arroz", "Carne", "Tomate", "Cebolla", "Leche", "Zanahoria"])

    def generar_unidad_medida(self) -> str: # Método #8
        """Método que permite generar el nombre de una unidad de medida aleatoria."""

        # Retorno de un nombre de una unidad de medida aleatoria
        return random.choice(["gramo", "libra", "unidad", "litro", "paquete"])

    def generar_valor_unidad(self) -> str: # Método #9
        """Método que permite generar el valor de una unidad aleatoria."""

        # Retorno del valor de una unidad aleatoria
        return str(random.randint(500, 20000))

    def generar_sitio_compra(self) -> str: # Método #10
        """Método que permite generar un sitio de compra aleatoria."""

        # Retorno de un nombre de sitio de compra aleatorio
        return random.choice(["Plaza de mercado", "Supermercado Éxito", "D1", "Justo & Bueno", "Plaza Paloquemao", 'Surtimax', 'PriceSmart', 'Carulla'])

    def generar_ingrediente_dict(self) -> dict: # Método #11
        """Método que permite generar un ingrediente, con información adicional aleatoria."""

        # Retorno de un ingrediente e información adicional aleartorio
        return {"nombre": self.generar_ingrediente_nombre(),
                "unidad": self.generar_unidad(),
                "valor": self.generar_valor(),
                "sitioCompra": self.generar_sitio_compra(),}

if __name__ == "__main__":
    # Instanciar FakerRecetarui
    faker = FakerRecetario()

    # Imprimir datos sobre la receta
    print("=== RECETA ===")
    print("Nombre receta:", faker.dar_receta_nombre())
    print("Tiempo:", faker.dar_tiempo())
    print("Personas:", faker.dar_personas())
    print("Calorías:", faker.dar_calorias())
    print("Preparación:", faker.dar_preparacion())
    print("Receta completa dict:", faker.dar_receta_dict())

    # Imprimir datos sobre el ingrediente
    print("\n=== INGREDIENTE ===")
    print("Nombre ingrediente:", faker.dar_ingrediente_nombre())
    print("Unidad:", faker.dar_unidad())
    print("Valor:", faker.dar_valor())
    print("Sitio de compra:", faker.dar_sitio_compra())
    print("Ingrediente completo dict:", faker.dar_ingrediente_dict())