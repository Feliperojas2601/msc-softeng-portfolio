# Cypress Random Tester (Monkey)

Este repositorio contiene el código para un monkey aleatorio desarrollado utilizando [Cypress](https://www.cypress.io/), un ejecutor de pruebas End to End construido sobre JavaScript. Usamos esta tecnología debido a la facilidad para gestionar páginas web en una variedad de navegadores, incluyendo Chrome, Canary, Edge, Electron, etc., y su funcionalidad de grabar y reproducir. La idea del monkey es simular acciones aleatorias de un usuario dentro de la Aplicación Bajo Pruebas (ABP) —en este caso, el sistema Ghost
— tales como clics, desplazamientos, entradas de texto, navegación o cambios de tamaño de ventana. Estas acciones permiten descubrir fallos inesperados o excepciones no manejadas sin necesidad de definir previamente casos de prueba específicos.

Este repositorio está basado en la implementación de [TheSoftwareDesignLab/monkey-cypress](https://github.com/TheSoftwareDesignLab/monkey-cypress).

## Requisitos

- Node.js (v20 o superior). Recomendamos usar lts/iron.
- npm o yarn para la gestión de dependencias.

## Cómo ejecutar
Para usar el monkey, debes seguir estos pasos:

- **Ejecutar ghost localmente**: Debe ejecutar con docker la versión 5.130 de la imagen de ghost en el puerto 3001 de su máquina local.

    ```bash
    docker run --name my-ghost -e NODE_ENV=development -e url=http://localhost:3001 -e security__staffDeviceVerification=false -p 3001:2368 ghost:5.130 
    ```

- **Crear usuario administrador**: El monkey fue modificado para que cree un usuario administrador en caso de que no exista o que inicie sesión con ese usuario. 

- **Instalar los módulos requeridos**

    ```bash
    # using npm
    npm install
    # using yarn
    yarn install
    ```

- **Configurar los parámetros deseados**: La carpeta raíz del repositorio contiene los archivos de configuración de Cypress (`cypress.config.js`), los cuales incluyen los parámetros de configuración para el monkey aleatorio.

    ```javascript

    const { defineConfig } = require("cypress");

    module.exports = defineConfig({
        e2e: {
            baseUrl: "http://localhost:3001/ghost",
        },
        env: {
            seed: 0xf1ae533d,   
            delay: 1000,        
            email: 'testmonkey@email.com',
            password: 'testmonkey',
            actions: {
                click: 0,       
                scroll: 0,     
                keypress: 0,   
                viewport: 0,    
                navigation: 0, 
                smartClick: 0,     
                smartCleanup: 0,  
                smartInput: 0,      
            },
        },
    });

    ```

- **Ejecutar el monkey**: Los comandos para ejecutar las pruebas deben ejecutarse desde la carpeta raíz.

    ```bash
    npm run test:ui
    # Ejecución en modo headless
    npm run test
    ```
    Nota: El navegador predeterminado es Electron 78 en modo headless. Para probar con otro navegador, agrega la opción `--browser <nombre-o-ruta-del-navegador>` al comando de ejecución, indicando cuál de los [navegadores soportados](https://docs.cypress.io/guides/guides/launching-browsers.html#Browsers) deseas usar.


## Configuración

Después de evaluar una serie de posibles eventos, definimos las siguientes 5 categorías básicas en las que los eventos podrían agruparse:

- **Eventos de Clic Aleatorio**: Clic izquierdo, derecho o doble clic, así como desplazamientos (_mouseover_) realizados a un elemento desde una posición aleatoria.
- **Eventos de Desplazamiento**: Desplazar la página hacia arriba, abajo, a la izquierda o a la derecha.
- **Eventos de Teclado**: Introducir un carácter (alfanumérico) o un carácter especial (`Enter`, `Supr`, `Esc`, `Backspace`, `Flechas`) con modificadores (`Shift`, `Alt` o `Ctrl`) dentro de un elemento enfocado. Es equivalente a presionar una tecla del teclado al enfocar un elemento.
- **Eventos de Navegación de Página**: Navegación típica que un usuario podría realizar, como ir a la página anterior o a la siguiente en la pila de navegación.
- **Eventos del Navegador**: Eventos que cambian la configuración del navegador, como cambiar el tamaño de la ventana.

Adicionalmente, hay 3 categorías _más inteligentes_ que pueden incluirse en las ejecuciones:

- **Eventos de Clic Aleatorio Inteligente**: Clic izquierdo, derecho o doble clic, así como desplazamientos (_mouseover_) realizados a un elemento _clickeable_ (`<a>`, `<button>`, `<input>`).
- **Eventos de Limpieza Inteligente**: Eventos que limpian la configuración del navegador (cookies, almacenamiento local) o limpian un campo `<input>`.
- **Entrada Inteligente**: Introduce diferentes tipos de valores (frases, correos electrónicos, contraseñas, fechas, números) en un campo `<input>` dependiendo de su tipo.

## Reportes

El monkey está configurado para usar [Mochawesome](https://www.npmjs.com/package/cypress-mochawesome-reporter) como herramienta de reporte. Por defecto, el reporte contendrá la secuencia de eventos intentados que se ejecutaron y un video de la ejecución.

## Modificaciones realizadas. 
- Registro de usuario administrador y/o inicio de sesión de manera autónoma en el monkey.
- Durante las primeras 2 ejecuciones se detectó un error relacionado con la función `clearInput` y `rInput`. Luego de eso se realizó un cambio a las funciones para que se omita el error en caso de no encontrar un input en una pantalla que no lo tenga.