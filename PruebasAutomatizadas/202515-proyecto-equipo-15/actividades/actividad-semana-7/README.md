# Informe de Actividad - Semana 7

## Participantes

| Nombre Completo | Correo Electrónico |
|-----------------|------------------- |
| Felipe Rojas | jf.rojasc123@uniandes.edu.co |
| Camilo Roa | ca.roac@uniandes.edu.co |

---

## Informe Actividades

## Descripción de Estrategias Utilizadas

Se configuraron tres estrategias de generación de datos para soportar las pruebas automatizadas, cada una utilizando herramientas específicas según el tipo de dato requerido:

### Data pool a-priori
- Para esta estrategia se utilizaron esquemas creados en Mockaroo, generando archivos JSON por funcionalidad.
- Cada archivo se almacena dentro de la carpeta data/ con el formato F00X_apriori.json, y es consumido secuencialmente durante la ejecución de los escenarios.

### Data pool dinámico (online)
- Se integró el API de Mockaroo para obtener datos en tiempo real durante la ejecución de las pruebas.
- Cada test consulta el esquema correspondiente mediante una llamada HTTP, obteniendo datos renovados en cada corrida de manera controlada.

### Data pseudo-aleatoria
- El proyecto utiliza la librería @faker-js/faker, configurada con una semilla fija para garantizar reproducibilidad.
- Faker permite generar datos pseudoaleatorios para los escenarios que requieren valores variados, pero determinísticos entre ejecuciones.

Posteriormente, la carpeta de tests o features fue dividida en 3 subcarpetas, una por cada tipo de generación, esto para presentar una diferencia clara entre los tests, cuyos escenarios en su gran mayoría se comparten y solo cambian la fuente de generación de datos.

---

## Escenarios inválidos

Se modelaron 5 escenarios que buscaban representar un uso indebido de la aplicación, estos escenarios están relacionados a las 5 funcionalidades iniciales pero se ubicaron en un archivo de test diferente. Así mismo, se creo un archivo .json diferente para almacenar los datos inválidos utilizados en cada uno de estos escenarios, la descripción de cada escenario es: 

- EI01: Crear una publicación con un título largo <255 carácteres, no hay un mensaje de error para el usuario
- EI02: Crear una página con un título largo <255 carácteres, no hay un mensaje de error para el usuario
- EI03: Crear una etiqueta con un título largo <255 carácteres
- EI04: Crear una etiqueta con un slug que contengan carácteres especiales como ? # y puedan representar un riesgo de seguridad
- EI05: Crear una etiqueta con un código de color no hexadecimal, el mensaje de error no está bien ubicado

Estas ejecuciones de pruebas fueron reportadas como incidentes en el repositorio del equipo.
 
---

## Listado de Funcionalidades

| ID | Funcionalidad | Descripción |
|----|---------------|-------------|
| F001 | Crear publicación. | Permite la generación y listado de publicaciones definiendo su título, contenido y metadatos. Esta funcionalidad representa la creación principal de contenido en Ghost. |
| F002 | Crear página. | Permite la generación y listado de páginas estáticas definiendo su título, contenido y metadatos. Esta funcionalidad representa la creación de la parte estructural del sitio. |
| F003 | Editar publicación. | Permite la actualización del contenido de una publicación existente, incluyendo cambios de título, texto, imágenes, entre otros. |
| F004 | Asignar etiqueta. | Vincula una etiqueta existente a una publicación y/o página, permitiendo categorizar el contenido. |
| F005 | Eliminar publicación. | Permite eliminar una publicación del sitio, asegurando que su contenido deje de estar disponible. |

---

## Listado de Escenarios

| ID   | ID Funcionalidad | Estrategias de Generación de Datos | Herramienta | Enlace Incidencias |
|------|------------------|------------------------------------|-------------|--------------------|
| E001 | F001 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E002 | F001 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E003 | F001 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E004 | F001 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E001 | F002 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E002 | F002 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E008 | F003 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E009 | F003 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E010 | F003 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E011 | F004 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/24) |
| E012 | F004 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/23) |
| E013 | F005 | Data-a-priori, dinamico, pseudo-aleatorio | Playwright, faker, mockaroo | |
| E001 | F001 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E002 | F001 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E003 | F001 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E004 | F001 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E001 | F002 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E002 | F002 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E008 | F003 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E009 | F003 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E010 | F003 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| E011 | F004 | Data-a-priori, pseudo-aleatorio | Kraken, faker | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/25) |
| E012 | F004 | Data-a-priori, pseudo-aleatorio | Kraken, faker | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/26) |
| E013 | F005 | Data-a-priori, pseudo-aleatorio | Kraken, faker | |
| EI01 | F001 | Data-a-priori | Playwright | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/22) |
| EI02 | F002 | Data-a-priori | Playwright | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/21) |
| EI03 | F004 | Data-a-priori | Playwright | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/20) |
| EI04 | F004 | Data-a-priori | Playwright | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/19) |
| EI05 | F004 | Data-a-priori | Playwright | [Incidencia](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/18) |

--

## Metodologia Estrategias

### Playwright 

En Playwright se implementaron tres estrategias de generación de datos, organizadas cada una en su propia carpeta dentro del directorio tests/:

tests/
 ├── apriori/
 ├── dinamico/
 └── pseudo/

#### Data a-priori

- Para cada funcionalidad (posts, pages, tags), se generó un archivo JSON propio utilizando Mockaroo, por ejemplo:
    - F001_apriori.json
    - F002_apriori.json
    - F003_apriori.json
- Estos archivos contienen registros predefinidos con campos como post_title, post_content, new_post_title, etc.
- Los tests dentro de la carpeta apriori/ leen los archivos, extraen los datos de un registro y son incorporados en las variables que van a ingresar el contenido dentro del post, page o tag.
- Se incorporó un índice incremental por ejecución para garantizar que cada test utilice un registro distinto del data pool.

#### Data dinámico (Online)

- Para datos dinámicos se crearon los esquemas: 
    - Se indicaron los campos con sus respectivos tipos de dato.
    - Se selecciono el tipo de archivo siendo este .json.
    - Se guarda el esquema y se habilita para que sea publico.
    - Se extrae la API y se incorpora dentro del archivo .env.
- Por decisión de diseño, el schema específico se declaró como una constante dentro del archivo del test.

#### Pseudo-aleatorio

- La carpeta tests/pseudo/ contiene las pruebas basadas en faker.js, ya implementadas en entregas anteriores, en el que se recibe una semilla que garantiza el comportamiento determinista en las pruebas.

#### Oráculo de pruebas en Playwright

- En Playwright el oráculo se implementó utilizando las aserciones de expect provistas por @playwright/test.
- Independientemente de la estrategia de generación de datos (pseudo-aleatoria con Faker, data pool a-priori o datos dinámicos desde Mockaroo), el criterio de verificación fue siempre el mismo: validar el estado visible en la interfaz de Ghost.
- Así, el oráculo está basado en el comportamiento observable del sistema (títulos y estados en la UI), y no en detalles internos de implementación. Lo único que cambia entre estrategias es cómo se generan los datos de entrada, pero las aserciones (expect(...)) se mantienen idénticas.

### Kraken

#### Data a-priori

- Se ajustaron los archivos .feature reutilizando los escenarios existentes, ubicando los nuevos escenarios a-priori al final de cada archivo para mantener el orden y estructura original.
- Algunas sentencias principalmente aquellas relacionadas con ingresar títulos o contenidos en publicaciones, páginas o etiquetas fueron modificadas para que recibieran la información proveniente de los archivos JSON del data pool. Cada step ahora toma los valores proporcionados por data-pool.js e inserta dinámicamente los campos correspondientes en cada ejecución.
- Los escenarios a-priori se agregaron después de los escenarios pseudo-aleatorios, respetando la estructura original.
- Se renombraron los escenarios para identificar claramente que pertenecen a la estrategia.

#### Pseudo-aleatorio

- Se mantuvo Faker, exactamente como venía configurado en las entregas previas.
- Se dejó el seed controlado desde properties.json.

#### Oráculo de pruebas en Kraken
- En Kraken el oráculo se implementó con las aserciones de Chai (expect), dentro de los step definitions asociados a los pasos Then de los archivos .feature.
- Al igual que en Playwright, la lógica del oráculo en Kraken es independiente de cómo se generen los datos (Faker o data pool a-priori): la fuente de datos cambia, pero lo que el oráculo valida siempre es el estado final del sistema observado en la interfaz.

#### Observaciones
- Por motivos de que la API gratuita de Mockaroo permite solo 200 peticiones, insuficiente para un proyecto completo de pruebas E2E, estos no fueron incluidos en Kraken. Su implementarción, habría causado fallas, mayor tiempo en revisiones, ajustes (horas-hombre) y costos adicionales.