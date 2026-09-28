# SnoozelessWeb

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 22.1.8.

## Pantallas implementadas

Maqueta navegable (NO funcional), pixel-perfect contra los mockups de Figma ("snoozeless - mockups - web"), Angular Material + tokens de `src/styles/`:

| Ruta | Pantalla | Nodo Figma |
| --- | --- | --- |
| `/login` | Inicio de sesión | `116:101` - W01-login |
| `/perfil` | Perfil | `116:137` - W01-perfil |
| `/dashboard` | Dashboard | `121:44` - W02-Dashboard |
| `/alarma/:id` | Detalle de alarma | `121:107` - W02-detalle-alarma |
| `/alarma/:id/vivo` | Detalle de alarma en vivo (sonando) | `121:170` - W02-detalle-alarma-vivo |
| `/reto-escritura` | Reto de escritura para apagar la alarma | `121:236` - W03-reto-escritura |
| `/reto-completado` | Reto completado con éxito | `227:464` - W03-reto-completado |

`reto-escritura` incluye validación en vivo (prevención de errores): el campo pasa a estado de error si lo escrito deja de coincidir con la frase objetivo, y navega automáticamente a `/reto-completado` en cuanto el texto coincide exactamente con la frase objetivo.

`/login` es la ruta raíz (`''` redirige a `/login`). Flujo completo navegable con clics, sin editar la URL: `/login` → (Continuar con Google/Apple) `/dashboard` → (Ver detalle) `/alarma/:id` → (Simular: la alarma está sonando) `/alarma/:id/vivo` → (Ir al reto) `/reto-escritura` → (al completar la frase) `/reto-completado` → (Ir al dashboard) `/dashboard`.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
