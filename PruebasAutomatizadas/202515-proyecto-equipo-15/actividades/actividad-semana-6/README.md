# Informe de Actividad - Semana 6

> [!NOTE]
> **Importante:** En caso de tener archivos multimedia, utilicen un gestor de contenidos (_Google Drive, YouTube, etc._) donde se evidencie la última fecha de edición y agreguen los enlaces al informe.
> Enlace de archivos multimedia: [Enlace - Semana 6](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgCfuwLbjSuaSZmdX3LsDFL6AWhpSjLD2Gadnr6heK00YiA?e=yWqpNZ)

## Participantes

| Nombre Completo       | Correo Electrónico         |
|-----------------------|----------------------------|
| Felipe Rojas | jf.rojasc123@uniandes.edu.co |
| Camilo Roa | ca.roac@uniandes.edu.co |

## Informe Actividades

> [!NOTE]
> ## Resumen de actividades de la semana
> Describa **brevemente** las actividades realizadas durante la semana, los logros alcanzados y cualquier desafío encontrado.
> 1. Comprensión de las herramientas y librerías utilizadas
>     - Se estudiaron las librerías de comparación de imágenes asociadas a cada una de las herramientas utilizadas para la ejecucion de las pruebas y de la entrega de la semana pasada: Pixelmatch (para Kraken) y Resemble.js (para Playwright)..
>     - El objetivo principal fue entender cómo generar los resultados finales y cómo contrastar capturas entre diferentes ejecuciones y versiones de Ghost.
> 2. Diseño de la metodología para la captura de pantallas
>   - El screenshot se almacena en una carpeta con la sintaxis: escenario/función/step y con su nombre de forma que sea mas sencillo comparar las capturas entre la versiones base y rc. 
> 3. Integración de Pixelmatch y Resemble.js en Kraken y Playwright
>     - Se implementó la lógica necesaria para que cada herramienta pudiera:
>         - Descargar las imágenes base y las imágenes de la versión release: Se definió un mecanismo estándar para obtener capturas antes y después de cada paso crítico de las pruebas automatizadas, para Playwright a partir de un pageObject antes y despues de su ejecucion. En Kraken se implementó un hook before encargado de realizar automáticamente estas capturas, garantizando su consistencia.
>         - Compararlas aplicando un threshold previamente definido.
>         - Generar un reporte con los resultados de las diferencias detectadas.
>     - Estas integraciones permitieron comparar visualmente comportamientos entre Ghost 4.5.0 (versión base) y Ghost 5.130 (versión release).
> 4. Implementación de una semilla (seed) para la generación de datos
>     - Se añadió una semilla compartida para que los datos generados mediante Faker o textos aleatorios fueran idénticos en ambas versiones de Ghost.
>     - Sin esta estandarización, muchas pruebas habrían fallado por variaciones en los inputs más que por diferencias reales entre versiones.
> 5. Generación y análisis del reporte de comparación
>     - Se creó un reporte que resume:
>         - Número de pruebas exitosas y fallidas.
>         - Nivel de diferencia entre imágenes según el threshold definido.
>     - Se estableció una regla:
>         - Si todas las pruebas pasan el umbral, la suite se considera exitosa.
>         - Si alguna falla, toda la ejecución se marca como fallida, permitiendo un criterio estricto de comparación entre versiones.
> 6. Manejo anticipado de errores relacionados con el registro en Ghost
>     - Durante las ejecuciones se detectó que algunas pruebas fallaban porque el proceso de registro en Ghost se completaba demasiado rápido o quedaba en un estado inconsistente.
>     - Se implementó lógica para validar:
>         - La URL posterior al registro exitoso.
>         - La presencia de un banner de advertencia.
>     - Si estos elementos aparecían a pesar de haber completado el registro, se redirigía automáticamente al flujo de sign-in, evitando bloqueos del flujo de prueba.
> 7. Ajustes para mejorar la estabilidad de las pruebas
>     - Se evaluaron y aplicaron mejoras como:
>         - Incremento del tiempo de espera (timeouts) para permitir que el DOM cargara adecuadamente.
>         - Ajustes en los tiempos de interacción para evitar condiciones de carrera.
>     - Estas mejoras redujeron la cantidad de fallas aleatorias y ayudaron a obtener resultados más confiables.
> 8. Interpretación final de resultados y fortalecimiento del entendimiento técnico
>     - Se analizaron los reportes generados para comprender mejor el comportamiento visual de las aplicaciones bajo prueba.
>     - Se profundizó en cómo funcionan las librerías de comparación de imágenes y en cómo interpretar los datos cuantitativos obtenidos.
>     - Esto permitió obtener un entendimiento más claro de las diferencias entre versiones y de la integridad de las pruebas automatizadas.

## Listado de Funcionalidades

| ID | Funcionalidad | Descripción |
|----|------------|----------------|
| F001 | Crear publicación. | Permite la generación y listado de publicaciones definiendo su título, contenido y metadatos. Esta funcionalidad representa la creación principal de contenido en Ghost. |
| F002 | Crear página. | Permite la generación y listado de páginas estáticas definiendo su título, contenido y metadatos. Esta funcionalidad representa la creación de la parte estructural del sitio. |
| F003 | Editar publicación. | Permite la actualización del contenido de una publicación existente, incluyendo cambios de título, texto, imágenes, entre otros. |
| F004 | Asignar etiqueta. | Vincula una etiqueta existente a una publicación y/o página, permitiendo categorizar el contenido. |
| F005 | Eliminar publicación. | Permite eliminar una publicación del sitio, asegurando que su contenido deje de estar disponible. |

## Listado de Escenarios

| ID    | ID Funcionalidad  | Versiones | Descripción | 
|-------|-------------------|---------- | ----------- | 
| E001 | Crear publicación básica con éxito | v4.5.0 y v5.130 | Crear una publicación con título y párrafos de texto como contenido de manera exitosa. |
| E006 | Crear página básica | v4.5.0 y v5.130 | Crear una página con título y párrafos de texto como contenido de manera exitosa. | Crear página |
| E008 | Editar título de una publicación | v4.5.0 y v5.130 | Crear una publicación básica, ir al listado de publicaciones, seleccionarla y modificar el título de manera exitosa | 
| E011 | Asignar etiqueta a publicación | v4.5.0 y v5.130 | Crear una publicación básica, crear una etiqueta y asignarla a la publicación. | 
| E013 | Eliminar publicación | v4.5.0 y v5.130 | Crear una publicación básica, ir al listado de publicaciones, seleccionarla y eliminarla, ir nuevamente al listado de publicaciones y confirmar que ha sido eliminada exitosamente. | 

## Resultados de Ejecución

| Ejecución | Enlaces a Incidencias | Comportamiento Actual | Comportamiento Esperado | Herramienta |
| --------- | --------------------- | --------------------- | ----------------------- | ----------- |
| Asignar etiqueta a publicación | [INC 012](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/13) | [Comportamiento Actual INC 012](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgDpcbcWKpFgRp6Ld5CU7oBVAdhCmsPBEZyFwHTzlzcxWjc?e=5ZavXm) | [Comportamiento Esperado INC 012](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgCjGMIU90XWSYacRZkblxIBAcxUDff3bXoEE-v8SJnI0uY?e=ypdh75) | Kraken (PixelMatch) |
| Crear página básica | [INC 013](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/14) | [Comportamiento Actual INC 013](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgDEwSi1zvJMT6drRXapRxOfAW-qeI8hJodGp-KINIQN9GI?e=EAj5t6) | [Comportamiento Esperado INC 013](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgDWDnfYZrzYR6dFrpzakP0pAV1hwDYyId22QNwm_aPdxzE?e=lPnLkZ) | Kraken (PixelMatch) |
| Crear publicación básica con éxito | [INC 014](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/15) | [Comportamiento Actual INC 014](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgA9KiB1xmBHQYwAglsddgzqAc0zyDH1gdrZK34kTqAF7Uw?e=WX5W2Y) | [Comportamiento Esperado INC 014](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgBj0AiK4pTTSbWchtcYvcsCAXnoLEQaTr0ycz62mQnnjEY?e=eF1mFF) | Kraken (PixelMatch) |
| Editar titulo de una publicación | [INC 015](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/16) | [Comportamiento Actual INC 015](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgDLf1ojn4OEQ5lUNenXr5nyAX068vacrP2-3NLFWZFzrU4?e=9WGtfX) | [Comportamiento Esperado INC 015](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgDLxiDd3J0_RoCVKBOqjFl9ATCeotW7DmiXUeu4WNXahLU?e=3hNbAx) | Kraken (PixelMatch) |
| Eliminar publicación basica | [INC 016](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/17) | [Comportamiento Actual INC 016](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgC74iN6xZ5pQJTzuFJXRnD3AX7IaoBV8nel7M0XAMNxTS8?e=1jQtrN) | [Comportamiento Esperado INC 016](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgBRNXmt6LdKTZZ_vYqcTTXiAdMeocwJujcpiknDGwW4Ct4?e=UxkkxK) | Kraken (PixelMatch) |
| Asignar etiqueta a publicación | [INC 012](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/13) | [Comportamiento Actual INC 012](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgCDq__V098FSb-yf_Nu00W5AaYxkPK2-a48AvNq4oHORgY?e=mnXHiJ) | [Comportamiento Esperado INC 012](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgDOLIq2lVZYSauPPgG-FB8EAc4VJbAn8pLF4tecEwOQez0?e=UJx4Xl) | Playwright (ResembleJS) |
| Crear página básica | [INC 013](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/14) | [Comportamiento Actual INC 013](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgCROoeK0z6rSYkx252xVTAqASDLkCs3cmELyc2QVfSRf-M?e=dRXLn1) | [Comportamiento Esperado INC 013](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgBEThUCTo18S6h8s_jkTpwUAS3Iw8bay-9eGDe2Hx0zOTE?e=TqMN8O) | Playwright (ResembleJS) |
| Crear publicación básica con éxito | [INC 014](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/15) | [Comportamiento Actual INC 014](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgC45zZL0aXLQYbCiuP5DzeOARaiionjNXgLrNIiRw6Ln64?e=Z1aXzD) | [Comportamiento Esperado INC 014](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgBhJDijf5b2SbPyLq8avh3fAe4506TGDS5J0uUpdAjamJY?e=sXqXIe) | Playwright (ResembleJS) |
| Editar titulo de una publicación | [INC 015](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/16) | [Comportamiento Actual INC 015](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgB2GjNs2wHRRLWU7Uw37UH9AUES2_2QtYDszhP0E34wp_0?e=jP6Qb8) | [Comportamiento Esperado INC 015](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgC9calDkoTqQJNlciBrE6YSAfCkQNxON_i5pmA1Nc_LhFI?e=ltXKeh) | Playwright (ResembleJS) |
| Eliminar publicación basica | [INC 016](https://github.com/Uniandes-MISW4103/202515-proyecto-equipo-15/issues/17) | [Comportamiento Actual INC 016](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgB6YbV5wR0GRoWKC_rmhQNkAVyXl9woUesR9cfggMWjENQ?e=0oYAHy) | [Comportamiento Esperado INC 016](https://uniandes-my.sharepoint.com/:f:/g/personal/ca_roac_uniandes_edu_co/IgDugextc61ZQoI6De8Yz0izAeKbJn3JS15dpPJOhomepdY?e=ADkoSG) | Playwright (ResembleJS) |



## Pros y Contras

### Herramienta VRT 1 - ResembleJS

#### Pros
- Ofrece métricas detalladas como misMatchPercentage, diffs con colores personalizables, y detalles que pueden proveer un análisis mas completo.
- Se identifico que puede utilizarse para evaluar diferencias, tanto por color, como brillo, y tolerancia.
- Generación automática de imágenes con diffs discernibles, produciendo imágenes de comparación más claras y explicativas.
- Configuración flexible del threshold: permite controlar con precisión qué tan estricta es la comparación.
- Su integración con Playwright resultó una decisión acertada, ya que facilitó la depuración, permitió acceder a ejemplos prácticos y ofreció una incorporación fluida y homogénea entre ambas herramientas.

#### Contras
- Su configuración inicial y entendimiento preliminar puede ser compleja y llevar un buen tiempo, sobretodo por lo que esta orientado a ejecuciones headless.
- No cuenta con una documentación clara.
- Consumo considerable de CPU.

### Herramienta VRT 2 - PixelMatch

#### Pros
- Permitio una incorporacion con Kraken que compensa el hecho de que esta herramienta al consumir menos recursos hizo que la ejecucion haya sido ligera y rapida.
- Se identifico que provee una comparacion estricta a nivel de pixeles.

#### Contras
- Provee una forma menos detallada o sencilla de comparar los diff, a comparacion de ResembleJS.
- La calidad del reporte es inferior.
- Provee mayor propensidad de errores.
- El reporte tiende a refrescarse despues de cierto tiempo y no permite 