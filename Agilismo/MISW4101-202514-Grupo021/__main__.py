# 1st Party Libraries
import sys
from src.vista.InterfazRecetario import App_Recetario
from src.logica.LogicaRecetario import LogicaRecetario

if __name__ == '__main__':
    
    # Punto inicial de la aplicación
    logica = LogicaRecetario()

    # Preparación de la app
    app = App_Recetario(sys.argv, logica)
    
    # Ejecución de la App
    sys.exit(app.exec_())