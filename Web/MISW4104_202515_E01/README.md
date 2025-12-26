# Frontend

Este proyecto fue generado con [Angular CLI](https://github.com/angular/angular-cli) versión 17.3.8.

## Servidor de desarrollo

Ejecuta `ng serve` para iniciar un servidor de desarrollo. Navega a `http://localhost:4200/`.  
La aplicación se recargará automáticamente cuando modifiques cualquiera de los archivos fuente.

## Generación de código

Ejecuta `ng generate component component-name` para generar un nuevo componente.  
También puedes usar `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Compilación

Ejecuta `ng build` para compilar el proyecto.  
Los artefactos resultantes se almacenarán en el directorio `dist/`.

## Ejecución de pruebas unitarias

Ejecuta `ng test` para correr las pruebas unitarias usando [Karma](https://karma-runner.github.io).

## Ejecución de pruebas end-to-end

Ejecuta `ng e2e` para correr las pruebas end-to-end usando cypress.

### Para tener en cuenta al ejecutar e2e

El backend del proyecto BackArte debe estar en ejecución para que el resultado de las pruebas sea exitoso. Las pruebas utilizan faker para la generación de datos aleatorios.

### Estadísticas del Suite de Pruebas

- **Total de Historias de Usuario**: 12
- **Total de Casos de Prueba Documentados**: 36
- **Page Objects Creados**: 11
- **Archivos de Prueba**: 11
- **Fixtures de Datos**: 4

---

## 📂 Estructura del Proyecto

```
cypress/
├── e2e/
│   ├── actors/
│   │   ├── actor-list.cy.ts          # HU01: Listado de actores
│   │   ├── actor-detail.cy.ts        # HU02: Detalle de actor
│   │   └── actor-create.cy.ts        # HU11: Crear actor
│   ├── directors/
│   │   ├── director-list.cy.ts       # HU03: Listado de directores
│   │   ├── director-detail.cy.ts     # HU04: Detalle de director
│   │   └── director-create.cy.ts     # HU12: Crear director
│   ├── genres/
│   │   ├── genre-list.cy.ts          # HU05: Listado de géneros
│   │   └── genre-create.cy.ts        # HU13: Crear género
│   └── movies/
│       ├── movie-list.cy.ts          # HU07: Listado de películas
│       ├── movie-detail.cy.ts        # HU08: Detalle de película
│       └── review-create.cy.ts       # HU16: Crear reseña
├── pages/
│   ├── BasePage.ts                   # Page Object base
│   ├── ActorListPage.ts
│   ├── ActorDetailPage.ts
│   ├── ActorCreatePage.ts
│   ├── DirectorListPage.ts
│   ├── DirectorDetailPage.ts
│   ├── DirectorCreatePage.ts
│   ├── GenreListPage.ts
│   ├── GenreCreatePage.ts
│   ├── MovieListPage.ts
│   └── MovieDetailPage.ts
├── fixtures/
│   └── data/
│       ├── actors.json
│       ├── directors.json
│       ├── genres.json
│       └── movies.json
└── support/
    ├── commands.ts                   # Comandos personalizados
    └── e2e.ts                        # Configuración global
```

---

## Más ayuda

Para obtener más ayuda sobre Angular CLI, usa `ng help` o visita la página de [Angular CLI Overview and Command Reference](https://angular.io/cli).
