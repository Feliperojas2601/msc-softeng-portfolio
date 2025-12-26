# Informe de Actividad - Semana 4

## Participantes

| Nombre Completo | Correo Electrónico |
|-----------------|--------------------|
| Felipe Rojas    | jf.rojasc123@uniandes.edu.co |
| Camilo Roa      | ca.roac@uniandes.edu.co      |

---

## Pruebas de Reconocimiento con Monkey.

### Informe Actividades

Durante esta semana se realizaron las configuraciones necesarias para ejecutar pruebas de reconocimiento sobre la Aplicación Bajo Pruebas (Ghost) utilizando la herramienta **Monkey** desarrollada sobre **Cypress**.  
Se implementó la lógica de inicio de sesión o registro automático según el estado del sistema, garantizando que la ejecución sea autónoma desde cero.  
Se logró ejecutar la herramienta con unas semillas iniciales para validar el comportamiento pseudoaleatorio y registrar los primeros incidentes relacionados a los eventos aleatorios y su implementación. Durante las primeras 2 ejecuciones se detectó un error relacionado con la función `clearInput` y `rInput`.
Luego de eso se realizó un cambio a las funciones para que se omita el error en caso de no encontrar un input en una pantalla que no lo tenga.

### Resultados de Ejecución

| Semilla de Ejecución | Observaciones | Enlaces a Evidencias | Enlace a Incidencias |
|----------------------|----------------------|----------------------|----------------|
| 0xf1ae533d | Error: `Timed out retrying after 4000ms: Expected to find element: input, but never found it.` El error se presenta en la función `clearInput`, cuando intenta limpiar un campo `input` que no existe en el DOM al momento de la interacción. | [Video de ejecución](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EVO5sO_iK1FMkF5FdsLrMRcBWUTUGwthZM_DzfnxeB5lLQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=DggK7P) | [Video de incidencia](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EVO5sO_iK1FMkF5FdsLrMRcBWUTUGwthZM_DzfnxeB5lLQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=DggK7P) |
| 0xdeadbeef | Error: `AssertionError: Timed out retrying after 4000ms: Expected to find element: input, but never found it.` El error se presenta en la función `rInput`, cuando intenta obtener un campo `input` que no existe en el DOM al momento de la interacción. | [Video de ejecución](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EcoWqBQ8CF9PnmC6wGtLBKIBY6f45Iw3VNe_NKny8jtxMg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=53INb7) | [Video de incidencia](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EcoWqBQ8CF9PnmC6wGtLBKIBY6f45Iw3VNe_NKny8jtxMg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=53INb7) |
| 0x1f2e3d4c | Error: `Request was rejected because user is not permitted to perform this operation.` El error se presenta en la etición "GET /ghost/api/admin/users/me/?include=roles". Siendo un usuario administrador es importante revisar este permiso faltante. | [Video de ejecución](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EahR_9p1JNhOkNrZnRxvUlIBG1FIBrsaIw3r6MGreeoIhQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=hWYoRv) | [Video de incidencia](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EahR_9p1JNhOkNrZnRxvUlIBG1FIBrsaIw3r6MGreeoIhQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=hWYoRv) |
| 0x4b7a91c3 | Sin errores. | [Video de ejecución](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EcxTup-veepMi0Aar5zZEs0BL-9W196zJA5KmR5y2ASlsw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=1QnCNX) | |
| 0xa93f12d7 | Sin errores. | [Video de ejecución](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EWXCR7O1o-dKv3oMoPgxU9gB-sF1GGgYkxKbVA4Icx9Ksw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=EdcWxp) | |
| 0x7bc41e99 | Sin errores. | [Video de ejecución](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_roac_uniandes_edu_co/EQZuZWvWdn9Hg6kcsWNj83gBl7Zb6bomQLkeru8bBahVhw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=n78lTS) | |

### Pros y Contras de la Herramienta

**Pros:**
- De fácil ejecución y de bajo costo en los recursos computacionales.
- Permite explorar rutas y comportamientos inesperados sin intervención humana.  
- Reproduce los resultados gracias al uso de semillas.  
- De alta personalización en el listado de eventos pseudo aleatorios que pueden realizarse. 
- Integración con Cypress y generación automática de videos y reportes.  

**Contras:**
- Los eventos aleatorios pueden generar errores falsos positivos al interactuar con elementos no visibles o no existentes.  
- La configuración inicial de algunas funciones genera errores inesperados al buscar elementos que pueden no estar en todas las partes del ABP.
- Requiere múltiples ejecuciones para obtener buena cobertura funcional. 

---

## Pruebas de Reconocimiento con Ripper.

### Informe Actividades

Durante esta semana se realizaron las configuraciones necesarias para ejecutar pruebas de reconocimiento sobre la Aplicación Bajo Pruebas (Ghost) utilizando la herramienta **Ripper** desarrollada sobre **Playwright**.  
Se integró la lógica de inicio de sesión o registro automático según el estado actual del sistema, permitiendo que la ejecución se adapte de forma autónoma en la función `navigateToDashboard`.  
Se logró realizar una única ejecución del Ripper, la cual evidenció la correcta interacción inicial con la interfaz del sistema y el reconocimiento de rutas de Ghost ej: members, tags, posts. La exploración es de un tiempo considerable por el tamaño de la aplicación Ghost.
No se utilizaron semillas pues su único uso en el caso del Ripper sería la misma generación de datos en formularios.


### Resultados de Ejecución

| Semilla de Ejecución | Observaciones | Enlaces a Evidencias | Enlaces a Incidencias |
|----------------------|----------------------|----------------------|----------------|
| - | Se evidencia el gran grafo de hipervínculos en la aplicación y capturas de algunos momentos de la exploración. Para el state #4 hay dos errores relacionados a la sección de posts y la carga de contenido en el editor.  | [Carpeta de reporte](../../reconocimiento/misw-4103-ripper/visibleResults/ripper) | [Reporte](../../reconocimiento/misw-4103-ripper/visibleResults/ripper/report.html) |


### Pros y Contras de la Herramienta

**Pros:**
- Permite recorrer la aplicación de forma estructurada y sistemática, identificando todas las rutas accesibles y elementos interactivos.
- Integra la automatización con Playwright, lo que ofrece control preciso sobre la exploración.
- Permite documentar el sistema con el grafo y capturas de pantalla.

**Contras:**
- Las ejecuciones son más lentas en comparación con el enfoque aleatorio de Monkey.
- Los reportes generados por la herramienta no son tan útiles y verbales.
