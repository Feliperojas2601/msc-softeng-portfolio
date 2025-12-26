

# Proyecto Base: Pruebas Visual Regression Testing (VRT) con ResembleJS

[ResembleJS](https://github.com/rsmbl/Resemble.js/blob/master/README.md) es una biblioteca de código abierto para comparación visual de imágenes. Es usada en procesos de prueba de regresión visual automatizada, donde se desea detectar diferencias entre dos capturas de pantalla o imágenes.

## Caracteristicas Principles:
1. *Comparación visual a nivel de píxel*
Detecta cambios precisos entre dos imágenes, resaltando diferencias por color, brillo, transparencia o desplazamientos.
2. *Imagen de diferencia (diff)*
Genera automáticamente una imagen que resalta las diferencias encontradas.
3. *Métricas cuantitativas*
Devuelve un porcentaje de diferencia (misMatchPercentage), útil para automatizar decisiones.
4. *Opciones de comparación avanzadas*
	- Ignorar antialiasing (suavizado).
	- Ignorar diferencias de color.
	- Ignorar canal alfa (transparencia).
	- Escalar imágenes para ajustarlas si tienen diferentes tamaños.
5. *Soporte para múltiples entornos*
	- Puede usarse en el navegador o en Node.js.


## Detalles adicionales:

1. *Región personalizada:* 
Se pueden comparar solo partes específicas de las imágenes usando coordenadas.
2. *Output configurable:* Personalización del color de las diferencias, transparencia del dif, o formato de imagen resultante.
3. *Integración con herramientas de testing:* 
Muy utilizado junto con frameworks como Playwright, Puppeteer o Cypress para verificar visualmente cambios en interfaces.


## Requisitos Básicos

- Node.js (versión 20 o superior). Recomendamos utilizar la versión `lts/iron`.
- npm o yarn para la gestión de dependencias.

## Instalación

Instala las dependencias necesarias utilizando npm:

```bash
npm install
```

## Configuracion

Para la libreria de ResembleJS: 

```bash
npm install resemblejs
```

Para que resemblejs funcione correctamente con canvas, necesitas tener instaladas ciertas bibliotecas:

```bash
npm install canvas
```
Canvas se encarga de comparacion de pixeles entre imagenes.

En el codigo consiste simplemente es llamar la libreria:

```javacript
const resemble = require('resemblejs');
```

y la comparacion consiste en ajustar las configuracion para determinar que tan exacta puedo comparar las imagenes:

vconst compareImages = require("resemblejs/compareImages");
const fs = require("mz/fs");

```javascript
async function getDiff() {
    const options = {
        output: {
            errorColor: {
                red: 255,
                green: 0,
                blue: 255
            },
            errorType: "movement",
            transparency: 0.3,
            largeImageThreshold: 1200,
            useCrossOrigin: false,
            outputDiff: true
        },
        scaleToSameSize: true,
        ignore: "antialiasing"
    };


    const data = await compareImages(await fs.readFile("./your-image-path/People.jpg"), await fs.readFile("./your-image-path/People2.jpg"), options);

    await fs.writeFile("./output.png", data.getBuffer());
}

getDiff();

```

## Ejecución de Pruebas e2e en la versión release y configuración adicional

Para la ejecución de la versión release con docker debe ejecutar:

```bash
docker run --name my-ghost -e NODE_ENV=development -e url=http://localhost:3001 -e security__staffDeviceVerification=false -p 3001:2368 ghost:5.130
```

Para obtener las carpetas con los screenshots debe ir a `e2e/misw-4103-playwright`, seguir la configuración de su README y ejecutar `npm run test`, verá luego de la ejecución exitosa de los tests la carpeta `screenshots-vrt`, renombrela a `screenshots-vrt-release` y copiela en `e2e/misw-4103-resemblejs/screenshots-vrt-release`.

### Linux
Puede usar las siguientes lineas de codigo para mover las carpetas ubicadas en e2e a vrt/misw-4103-pixelmatch de la siguiente forma:

- Version Base (Docker 5.130): 

```bash
mv e2e/misw-4103-playwright/screenshots-vrt vrt/misw-4103-resemblejs/screenshots-vrt-release
```

- Version Release (Docker 4.5.0): 

```bash
mv e2e/misw-4103-playwrigh-base/screenshots-vrt vrt/misw-4103-resemblejs/screenshots-vrt-base
```

Con el comando mv, tan pronto se haya especificado con exactitud la ubicacion de la carpeta donde se encuentran las capturas de pantalla, el siguiente parametro le permite ubicarla en la ruta que corresponde y al final de la ruta de la carpeta, se puede colocar el nombre que desee de las carpetas con los archivos, teniendo en cuenta el desarrollo exitoso de la prueba, los comandos presentados arriba generan el renombramiento de las carpetas como fue especificado en el apartado de la obtencion de las carpetas con los screenshots a fin de asegurar su correcta ejecucion.

## Ejecución de Pruebas e2e en la versión base y configuración adicional

Como se utiliza el mismo puerto y nombre de contenedor debe pausar y eliminar la ejecución anterior: 

```bash
docker stop my-ghost
docker rm my-ghost
```

## Linux

Para usuarios de Linux, debe detener y eliminar la imagen en Docker o asegurarse preferiblemente que no haya alguna en ejecución. 

Recuerde que con el comando sudo debe ingresar su contraseña de acceso al equipo. 

Con el fin de detener la imagen o alguna que posiblemente se encuentre en ejecución, utilice el siguiente comando:

```bash
sudo docker stop $(docker ps -aq)
```

Y para eliminar imagenes en Docker:

```bash
sudo docker rm $(docker ps -aq)
```

Para la ejecución de la versión base con docker debe ejecutar:

```bash
docker run --name my-ghost -e NODE_ENV=development -e url=http://localhost:3001 -e security__staffDeviceVerification=false -p 3001:2368 ghost:4.5.0
```

Para obtener las carpetas con los screenshots debe ir a `e2e/misw-4103-playwright-base`, seguir la configuración de su README y ejecutar `npm run test`, verá luego de la ejecución exitosa de los tests la carpeta `screenshots-vrt`, renombrela a `screenshots-vrt-base` y copiela en `e2e/misw-4103-resemblejs/screenshots-vrt-base`.

## Definición de Threshold 

El **threshold** es el porcentaje máximo de diferencia permitid* entre dos imágenes para considerar que son "iguales" visualmente. 

Edite la constante en `compare-screenshots.js`:

```javascript
const THRESHOLD = 10.0; // 10% de diferencia permitida
```

Consideramos que este valor de treshold ofrece estas posibilidades:
- **Tolera cambios menores**: Antialiasing, renderizado de fuentes, pequeñas variaciones de píxeles.
- **Tolera cambios medios**: Cambios en UI pequeños, elementos extra como notificaciones de la versión, etc.
- **Desfavorece cambios grandes**: Cambios en UI completos, secciones faltantes, etc.

## Ejecución de Pruebas Vrt y reporte

Asegurese de tener screenshots en ambas carpetas:
- `screenshots-vrt-base/` - Version Ghost 4.5.X
- `screenshots-vrt-release/` - Version actual 5.X

Dado que se utiliza un archivo JavaScript para la configuración de la herramienta, en el archivo **package.json** se definieron los siguientes comandos:

- Para ejecutar la comparación y generar el reporte utilice:

  ```bash
  # Ejecución de las pruebas de regresión visual utilizando el archivo backstop.js
  npm run vrt
  ```

Una vez terminada la ejecucion, Los resultados aparecen en `vrt-report/` tanto las imágenes comparadas como el index.html con la   presentación y resultados de la prueba. También se imprime en la consola un desglose general de los resultados.

```
🚀 Iniciando Visual Regression Testing con ResembleJS...

📊 Threshold configurado: 5.0%
   (Diferencias ≤ 5.0% = PASS, > 5.0% = FAIL)

📁 Imágenes encontradas en Base: 45
✅ Imágenes coincidentes para comparar: 42
⚠️  3 imagen(es) solo existen en Base y serán omitidas

🔍 Comparando [1/42]: f001/create_basic_post/step_01.png
   ✅ PASS - Diferencia: 2.34%

🔍 Comparando [2/42]: f001/create_basic_post/step_02.png
   ❌ FAIL - Diferencia: 8.92%

...

============================================================
📊 RESUMEN FINAL
============================================================
Total de comparaciones: 42
✅ Pruebas exitosas: 40
❌ Pruebas fallidas: 2
📈 Tasa de éxito: 95.24%
🎯 Threshold: 5.0%
⬆️ Diferencia máxima encontrada: 50%
============================================================

❌ RESULTADO: FAIL

📄 Reporte generado en: vrt-report/index.html
🖼️  Imágenes de diferencia en: vrt-report/diff-images
```
