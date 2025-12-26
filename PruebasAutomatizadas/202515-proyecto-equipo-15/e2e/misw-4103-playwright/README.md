# Proyecto Base: Pruebas End to End con Playwright

Playwright es un framework moderno y fácil de usar para realizar pruebas E2E. Ofrece una interfaz intuitiva y herramientas integradas para depuración. Es ideal para pruebas en aplicaciones web modernas.

Este repositorio cuenta con la configuración base de Playwright para la automatización de pruebas E2E.

## Requisitos Básicos

- Node.js (versión 20 o superior). Recomendamos utilizar la versión `lts/iron`.
- npm o yarn para la gestión de dependencias.

## Instalación

Instala las dependencias necesarias utilizando npm:

```bash
npm install
npm run prepare # Instala las demás dependencias de Playwright automáticamente.
```

## Ejecución de Ghost local

Debe ejecutar localmente ghost con docker antes de ejecutar las pruebas, utilice el siguiente comando.

```bash
docker run --name my-ghost -e NODE_ENV=development -e url=http://localhost:3001 -e security__staffDeviceVerification=false -p 3001:2368 ghost:5.130 
```

## Variables de Entorno

El proyecto utiliza variables de entorno para gestionar las credenciales de prueba. Debe crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
EMAIL=testmonkey@email.com
PASSWORD=testmonkey
FAKER_SEED=42
MOCKAROO_API_KEY=24e26fe0
```

## Imagen de prueba

El proyecto utiliza una imagen para gestionar algunos escenarios de pruebas. Debe crear un archivo `test-image.png` en la ruta `tests/test-data/`

## Ejecución de Pruebas

Puedes ejecutar las pruebas en modo headless o con interfaz gráfica del navegador:

- Para ejecutar las pruebas en modo headless:

    ```bash
    npm test
    ```

- Para ejecutar las pruebas con interfaz gráfica:

    ```bash
    npm run test:ui
    ```

## Configuración

El archivo de configuración principal de Playwright se encuentra en `playwright.config.js`. Este archivo define las opciones globales para las pruebas, como el directorio de pruebas, los navegadores soportados y las configuraciones específicas para cada proyecto.

Algunos puntos clave de la configuración:

- **Carga de variables de entorno**: Las pruebas utilizan variables cargadas con dotenv.
- **Directorio de pruebas**: Las pruebas se encuentran en el directorio `./tests`.
- **Ejecución en paralelo**: Las pruebas se ejecutan en paralelo para optimizar el tiempo de ejecución.
- **Base URL**: La URL base configurada es `http://localhost:3001/ghost`. Esto permite usar rutas relativas en las pruebas.
- **Reintentos**: En entornos CI, las pruebas fallidas se reintentan automáticamente hasta 2 veces.
- **Reportes**: Se genera un reporte en formato HTML tras la ejecución de las pruebas.
- **Navegadores soportados**: Actualmente, el proyecto está configurado para ejecutarse en Chromium con el perfil de "Desktop Chrome".

# Modificaciones realizadas al proyecto base

Se ha modificado el archivo ```playwright.config.js``` para: 
- Cambiar la url base del proyecto a la url de ejecución local de ghost.
- Instalar la depedencia dotenv y utilizarla para cargar variables de entorno.
- Aumentar el timeout de tests a 60s.