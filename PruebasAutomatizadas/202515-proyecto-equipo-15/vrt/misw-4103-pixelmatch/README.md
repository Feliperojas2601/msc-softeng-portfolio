
# Proyecto Base: Pruebas Visual Regression Testing (VRT) con Pixelmatch

[PixelMatch](https://github.com/mapbox/pixelmatch/blob/main/README.md) es una biblioteca de JavaScript para la comparación de imágenes a nivel de píxel, especialmente diseñada para detectar diferencias entre imágenes, por ejemplo, en pruebas de regresión. Es rápida y eficiente, trabajando con arrays de datos de imágenes y no dependiente de otras bibliotecas. 

## Caracteristicas Principles:
*Comparación de imágenes:*
Permite comparar dos imágenes y determinar la presencia de diferencias entre ambas. 

*A nivel de píxel:*
Analiza cada píxel individualmente para detectar diferencias. 

*Para pruebas:*
Ideal para comparar imágenes en pruebas de regresión, donde se busca detectar cambios no deseados. 

*Rápida y eficiente:*
Diseñada para ser rápida y no depender de otras bibliotecas, lo que la hace adecuada para pruebas automatizadas. 

## Detalles adicionales:

*Funciones de comparación:*
Incluye funciones para comparar imágenes basadas en la percepción del color (métricas de color perceptual) y para detectar píxeles antialiased. 

*Uso en pruebas automatizadas:*
Es común encontrarla en pruebas de integración continua, donde se comparan capturas de pantalla para asegurar que no haya cambios inesperados. 

*Implementación:*
Es una biblioteca relativamente pequeña y simple, con una implementación en alrededor de 120 líneas de código. 

*Versatilidad:*
Puede ser utilizada tanto en entornos de navegador como en entornos Node.js. 

## Requisitos Básicos

- Node.js (versión 20 o superior). 
   - Recomendamos utilizar la versión `lts/iron`.
- Docker (version 29.0.0 o superior).
- npm o yarn como gestor paquietes y dependencias.

## Instalación

Instala las dependencias necesarias utilizando npm:

```bash
npm install
```

## Ejecución de Pruebas e2e en la versión release y configuración adicional

Abra una terminal, y coloque el siguiente comando:

```bash
docker run --name my-ghost -e NODE_ENV=development -e url=http://localhost:3001 -e security__staffDeviceVerification=false -p 3001:2368 ghost:5.130
```

Para obtener las carpetas con los screenshots debe ir a `e2e/misw-4103-kraken`, seguir la configuración de su README y ejecutar `npm run test`, verá luego de la ejecución exitosa de los tests los que seran almacenados en la carpeta: `screenshots-vrt`, tan pronto finalicen las pruebas, renombrela a `screenshots-vrt-release` y copiela en `vrt/misw-4103-pixelmatch/screenshots-vrt-release`.

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

Para obtener las carpetas con los screenshots debe ir a `e2e/misw-4103-kraken-base`, seguir la configuración de su README y ejecutar `npm run test`, verá luego de la ejecución exitosa de los tests la carpeta `screenshots-vrt`, renombrela a `screenshots-vrt-base` y copiela en `vrt/misw-4103-pixelmatch/screenshots-vrt-base`.

### Linux
Puede usar las siguientes lineas de codigo para mover las carpetas ubicadas en e2e a vrt/misw-4103-pixelmatch de la siguiente forma:

- Version Base (Docker 5.130): 

```bash
mv e2e/misw-4103-kraken/screenshots-vrt vrt/misw-4103-pixelmatch/screenshots-vrt-release
```

- Version Release (Docker 4.5.0): 

```bash
mv e2e/misw-4103-kraken-base/screenshots-vrt vrt/misw-4103-pixelmatch/screenshots-vrt-base
```

Con el comando mv, tan pronto se haya especificado con exactitud la ubicacion de la carpeta donde se encuentran las capturas de pantalla, el siguiente parametro le permite ubicarla en la ruta que corresponde y al final de la ruta de la carpeta, se puede colocar el nombre que desee de las carpetas con los archivos, teniendo en cuenta el desarrollo exitoso de la prueba, los comandos presentados arriba generan el renombramiento de las carpetas como fue especificado en el apartado de la obtencion de las carpetas con los screenshots a fin de asegurar su correcta ejecucion.

## Definición de Threshold 

El **threshold** es el porcentaje máximo de diferencia permitido entre dos imágenes para considerar que poseen un alto grado o bajo grado de diferencia. 

Editelo en `vrt.config.json`:

```json
{
  "threshold": 0.1, // 10%
  "includeAA": true,
  "alpha": 0.1,
  "aaColor": [255, 0, 0],
  "diffColor": [255, 0, 255],
  "diffMask": false
}
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

- Dirijase a vrt/misw-4103-pixelmatch/

- Para ejecutar la comparación y generar el reporte utilice:

  ```bash
  # Ejecución de las pruebas de regresión visual utilizando el archivo backstop.js
  npm run vrt
  ```

Una vez terminada la ejecucion, los resultados aparecen en `vrt-report/` tanto las imágenes comparadas como el index.html con la presentación y resultados de la prueba. También se imprime en la consola un desglose general de los resultados.

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
