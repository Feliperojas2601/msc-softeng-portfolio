# Documentación del Proyecto

## Tabla de contenido

- [Documentación del Proyecto](#documentación-del-proyecto)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Equipo de trabajo](#equipo-de-trabajo)
    - [Nombre del grupo](#nombre-del-grupo)
    - [Líder del grupo](#líder-del-grupo)
    - [Integrantes](#integrantes)
    - [Reglas de equipo](#reglas-de-equipo)
  - [Tecnologías seleccionadas](#tecnologías-seleccionadas)
  - [Vistas de arquitectura](#vistas-de-arquitectura)
  - [Requerimientos (Entrega 2)](#requerimientos-entrega-2)
  - [Requerimientos (Entrega 3)](#requerimientos-entrega-3)

## Equipo de trabajo

### Nombre del grupo

clonatdevs

### Líder del grupo

Juan Felipe Rojas Cendales

### Integrantes

| Nombre | Usuario GitHub | Correo Uniandes | Rol actual | Intereses |
|---|---|---|---|---|
| Gabriela Zambrano Zuluaga | [Gabs-489](https://github.com/Gabs-489) | g.zambranoz@uniandes.edu.co | Estudiante de último semestre de pregrado de ingeniería de sistemas | Gestión de proyectos, toma de decisiones de tecnologías y/o funcionalidades según objetivos y recursos del proyecto, diseño de sistemas eficientes |
| Laura Pinzon Moreno | [LauraPi9](https://github.com/LauraPi9) | l.pinzonm2@uniandes.edu.co | Gestión, planeación y seguimiento de proyectos de ingeniería; preparación, revisión y gestión de procesos de contratación y licitaciones | Fortalecer habilidades en desarrollo de software, patrones de diseño y buenas prácticas; profundizar en computación en la nube y tecnologías cloud; aplicar lo aprendido en la maestría en su vida profesional |
| German Andres Gonzalez Ortega | [5ag5](https://github.com/5ag5) | ga.gonzalezo1@uniandes.edu.co | Analista de Producto: define arquitectura funcional (y técnica en algunos casos), requerimientos funcionales y apoya la creación del plan de pruebas | Creación de aplicaciones de alto rendimiento y eficiencia, optimizadas para mínimo consumo de memoria, mediante técnicas avanzadas de programación, patrones de arquitectura, principios de diseño, estructuras de datos, herramientas y algoritmos |
| Juan Felipe Rojas Cendales | [FelipeRojas5913](https://github.com/FelipeRojas5913) | jf.rojasc123@uniandes.edu.co | Desarrollador fullstack en GoPass: aplicación móvil general, migración a microservicios y aplicación para manejo de flotas | Arquitectura, liderazgo técnico, IA |

### Reglas de equipo

1. Se realiza un daily mínimo cada miércoles a las 18:00 para revisar avances, bloqueos y próximos pasos.
2. El equipo trabaja bajo una estrategia de ramificación Gitflow simplificada, con únicamente las ramas `main`/`master`, `feature/*` y `hotfix/*`.
3. Todo el código debe seguir buenas prácticas de desarrollo: nombres claros, funciones pequeñas y con una sola responsabilidad, y ausencia de código duplicado o muerto.
4. La comunicación entre los integrantes debe ser oportuna y respetuosa, informando bloqueos o retrasos el mismo día en que se identifican.
5. Ninguna rama se integra a `main` sin al menos una revisión de código aprobada por otro integrante y sin las pruebas unitarias correspondientes.

## Tecnologías seleccionadas

El equipo estandarizó las siguientes tecnologías para el desarrollo de las aplicaciones del sistema.

| Categoría | Tecnología | Uso |
|---|---|---|
| Lenguaje | Python 3.11 | Lenguaje de desarrollo de todas las aplicaciones |
| Framework web | FastAPI | Exposición del API REST de cada aplicación |
| Manejo de dependencias | Poetry | Gestión de dependencias y del entorno virtual de cada aplicación |
| Base de datos | PostgreSQL 16 en AWS RDS | Una única base de datos física, `clonatdevs`, con tablas lógicamente desacopladas y propiedad exclusiva de cada microservicio |
| ORM | SQLAlchemy (modo asíncrono) + asyncpg | Acceso a la base de datos desde las aplicaciones |
| Librería de pruebas | Pytest, pytest-cov, pytest-mock, pytest-asyncio | Pruebas unitarias y cobertura de código |
| Pruebas de API | Postman / Newman | Validación funcional del contrato de cada API |
| Contenerización | Docker | Empaquetado de cada aplicación en imágenes independientes |
| Orquestación | Kubernetes (Minikube y AWS EKS) | Minikube para desarrollo local y AWS EKS para el despliegue evaluado en la nube |
| Integración continua | GitHub Actions | Ejecución de linters, pruebas unitarias y validación de despliegue en cada entrega |
| Documentación como código | Markdown + PlantUML + Vale | Documentación técnica versionada y su validación automática |

## Vistas de arquitectura

- [Vista de información](./vista-informacion.md): datos que maneja el sistema y modelo de entidades.
- [Vista funcional](./vista-funcional.md): componentes del sistema y sus relaciones.
- [Vista de despliegue](./vista-despliegue.md): despliegue de los componentes y modelo de red.
- [Vista de desarrollo](./vista-desarrollo.md): estructura del proyecto y herramientas de desarrollo.

## Requerimientos (Entrega 2)

- [Patrones de solución por requerimiento](./patrones-solucion.md): tabla de patrones, justificación y atributos de calidad.
- Requerimiento RF-003 - Crear publicaciones
  - [Explicación paso a paso y modelo de secuencia](./requerimientos/rf-003.md)
  - [Patrones de solución](./patrones-solucion.md#rf-003---crear-publicaciones)
- Requerimiento RF-004 - Crear ofertas
  - [Explicación paso a paso y modelo de secuencia](./requerimientos/rf-004.md)
  - [Patrones de solución](./patrones-solucion.md#rf-004---crear-ofertas)
- Requerimiento RF-005 - Consultar publicaciones
  - [Explicación paso a paso y modelo de secuencia](./requerimientos/rf-005.md)
  - [Patrones de solución](./patrones-solucion.md#rf-005---consultar-publicaciones)
- [Vista Funcional: Modelo de Componentes](./vista-funcional.md)
  - [Componentes Nuevos](./vista-funcional.md#documentación-de-componentes-nuevos-entrega-2)
- [Vista de Despliegue: Modelo de Despliegue en la Nube](./vista-despliegue.md)

## Requerimientos (Entrega 3)

La arquitectura de RF-006 amplía las vistas de la entrega anterior. Su aplicación de tarjetas utiliza Flask y acceso síncrono a PostgreSQL; la tabla tecnológica anterior describe los servicios existentes de la entrega 2. La creación inicial de tarjetas está implementada; el Mediator, el polling, la outbox y la infraestructura de mensajería se mantienen como diseño propuesto hasta completar sus artefactos.

- Requerimiento RF-006 - Crear tarjetas de crédito
  - [Criterios, proceso paso a paso, datos y modelo de secuencia](./requerimientos/rf-006.md)
  - [Vista funcional y documentación de componentes nuevos](./requerimientos/rf-006.md#vista-funcional-y-componentes)
  - [Vista de despliegue, configuración y operación](./requerimientos/rf-006.md#vista-de-despliegue-y-operación)
  - [Patrón Mediator y patrones complementarios](./patrones-solucion.md#rf-006---crear-tarjetas-de-crédito)
- Requerimiento RF-007 - Verificar la identidad del usuario
  - [Explicación paso a paso y modelo de secuencia](./requerimientos/rf-007.md)
  - [Patrones de solución](./patrones-solucion.md#rf-007---verificar-la-identidad-del-usuario)
- [Vista Funcional: Modelo de Componentes](./vista-funcional.md)
  - [Componentes Nuevos](./vista-funcional.md#documentación-de-componentes-nuevos-entrega-3)
- [Vista de Despliegue: Modelo de Despliegue en la Nube](./vista-despliegue.md)
