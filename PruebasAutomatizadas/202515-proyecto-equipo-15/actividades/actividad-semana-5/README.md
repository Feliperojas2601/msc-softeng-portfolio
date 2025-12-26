# Informe de Actividad - Semana 5

## Participantes

| Nombre Completo | Correo Electrónico |
|-----------------------|------------------------------|
| Juan Felipe Rojas | jf.rojasc123@uniandes.edu.co |
| Camilo Roa| ca.roac@uniandes.edu.co|

---

## Informe Actividades

## Listado de Funcionalidades

| ID | Funcionalidad | Descripción |
|----|------------|----------------|
| F001 | Crear publicación. | Permite la generación y listado de publicaciones definiendo su título, contenido y metadatos. Esta funcionalidad representa la creación principal de contenido en Ghost. |
| F002 | Crear página. | Permite la generación y listado de páginas estáticas definiendo su título, contenido y metadatos. Esta funcionalidad representa la creación de la parte estructural del sitio. |
| F003 | Editar publicación. | Permite la actualización del contenido de una publicación existente, incluyendo cambios de título, texto, imágenes, entre otros. |
| F004 | Asignar etiqueta. | Vincula una etiqueta existente a una publicación y/o página, permitiendo categorizar el contenido. |
| F005 | Eliminar publicación. | Permite eliminar una publicación del sitio, asegurando que su contenido deje de estar disponible. |


## Listado de Escenarios

| ID | ID Funcionalidad | Descripción | Playwright | Kraken |
|----|------------------|-------------|------------|--------|
| E001 | Crear publicación básica. | Crear una publicación con título y párrafos de texto como contenido de manera exitosa. | ✅ | ✅ | 
| E002 |Crear publicación con imagen principal. | Crear una publicación con título, párrafos de texto como contenido y una imagen principal asociada a la publicación de manera exitosa. | ✅ | ✅ | 
| E003 | Crear publicación sin título. | Crear una publicación sin establecer un título y párrafos de texto como contenido de manera exitosa. | ✅ | ✅ | 
| E004 | Crear publicación sin contenido. | Crear una publicación con título y sin contenido de manera exitosa. | ✅ | ✅ |
| E005 | Crear publicación y programarla para publicación futura. | Crear una publicación con título y párrafos de texto como contenido y programarla para su publicación en 10 minutos de manera exitosa. | ✅ || 
| E006 | Crear página básica. | Crear una página con título y párrafos de texto como contenido de manera exitosa. | ✅ | ✅ | 
| E007 | Crear página con imagen principal. | Crear una página con título, párrafos de texto como contenido y una imagen principal asociada a la página de manera exitosa. | ✅ | ✅ | 
| E008 | Editar título de una publicación | Crear una publicación básica, ir al listado de publicaciones, seleccionarla y modificar el título de manera exitosa | ✅ | ✅ | 
| E009 | Editar imagen principal de publicación | Crear una publicación básica, ir al listado de publicaciones, seleccionarla y modificar la imagen de manera exitosa. | ✅ | ✅ | 
| E010 | Editar publicación al restaurar una versión previa | Crear una publicación básica, ir al listado de publicaciones, seleccionarla y modificar el título, ir nuevamente al listado de publicaciones y restaurarla a la versión anterior de manera exitosa. | ✅ | ✅ | 
| E011 | Asignar etiqueta a publicación. | Crear una publicación básica, crear una etiqueta y asignarla a la publicación. | ✅ | ✅ | 
| E012 | Asignar etiqueta a página. | Crear una página básica, crear una etiqueta y asignarla a la publicación. | ✅ | ✅ | 
| E013 | Eliminar publicación. | Crear una publicación básica, ir al listado de publicaciones, seleccionarla y eliminarla, ir nuevamente al listado de publicaciones y confirmar que ha sido eliminada exitosamente. | ✅ | ✅ | 


## Pros y Contras

### Playwright

#### Pros

Durante el desarrollo de la actividad, el uso de la herramienta Playwright resultó especialmente interesante y genero buenas impresiones.

- Brinda la posibilidad de ejecutar múltiples pruebas en simultáneo, permitiendo visualizar en tiempo real la secuencia de actividades y su respectivo estado de ejecución tanto en la terminal como en la interfaz gráfica. Este nivel de visibilidad facilita comprender con mayor claridad el flujo de pruebas y detectar posibles fallos de manera inmediata.
- Cada escenario ejecutado mediante la UI cuenta con su su propio "canvas" de navegador. 
- Presenta de forma amigable e intuitiva los errores y logs, lo cual facilita el proceso de depuración. A diferencia de otras herramientas, Playwright ofrece mensajes de error más claros y comprensibles, lo que reduce la dificultad de comprensión y favorece el mantenimiento del código.
- La herramienta está bien optimizada y permite ejecutar pruebas sin afectar el rendimiento general del equipo que la ejecuta, lo que posibilita continuar realizando otras tareas en paralelo sin interrupciones. 
- La interfaz gráfica de Playwright es moderna y accesible; por ejemplo, al hacer hover sobre los procesos en la barra lateral izquierda, se pueden visualizar detalles como el resultado de la prueba, el tiempo estimado de espera, y otros datos relevantes, lo que contribuye a una experiencia de usuario más eficiente y amigable.
- En cuanto a la generación del código, al ser un proyecto basado en node, se puede generar una organización/subarquitectura escalable y mantenible. También se pueden ejecutar los patrones Given/When/Then y PageObject con facilidad.
- La generación de reportes y evidencias es muy completa. Playwright permite crear reportes en formato HTML, incluir capturas de pantalla y almacenar videos y registros de ejecución.

Contras: 
- Playwright o genera automáticamente grabaciones .mp4 de las ejecuciones de prueba.
- La ejecución con solo la terminal puede ser confusa para identificar errores y hacer uso de pausas en las pruebas.
- Aunque cuenta con métodos de espera para ejecutar una acción hasta que un elemento se haya renderizado, principalmente cae en el antipatrón de tiempos de espera.  

#### Contras

- Cuando se ejecutan pruebas directamente desde la terminal, no fue posible pausar y retomar una prueba desde un punto intermedio, todas deben iniciarse desde el principio y esperar a su finalización. 
- Playwright o genera automáticamente grabaciones .mp4 de las ejecuciones de prueba.
- La ejecución con solo la terminal puede ser confusa para identificar errores y hacer uso de pausas en las pruebas.
- Aunque cuenta con métodos de espera para ejecutar una acción hasta que un elemento se haya renderizado, principalmente cae en el antipatrón de tiempos de espera. 

### Kraken

Durante el desarrollo de la actividad, el uso de la herramienta Kraken resultó especialmente interesante y retador.

####  Pros
- Permite ejecutar múltiples escenarios de pruebas en simultáneo, manteniendo la coherencia de cada escenario.
- El reporte generado por cada feature se presenta en HTML de manera completa.
- La herramienta permite la creación de escenarios de prueba utilizando la metodología BDD, los .feature generan una documentación viva y son legibles para todo tipo de roles.
- Los patrones Given/When/Then y PageObject están bien soportados con la organización/subarquitectura propuesta por Kraken.
- La herramienta está optimizada y no afecta el rendimiento del equipo local que la ejecuta.

####  Contras
- No presenta "canvas" separados por escenarios de prueba, los escenarios se ven sobrepuestos en un mismo navegador y esto puede ser confuso. 
- La presentación de errores y logs podría ser más amigable con el automatizador. 
- Debería contar con una funcionalidad7script para ejecutar solo un archivo .feature.
- Los reportes no se unifican por ejecución sino por feature.
- Podrían agregarse más parámetros de configuración.