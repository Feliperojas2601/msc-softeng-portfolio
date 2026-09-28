# Snoozeless - UX Mejoramiento de Experiencia del Usuario (Grupo #6)

Prototipos no funcionales, pixel-perfect contra los mockups de Figma, de la aplicación Snoozeless:

1. Implementar las interfaces de la aplicación **mobile** del proyecto como un prototipo no funcional.
2. Implementar las interfaces de la aplicación **web** del proyecto como un prototipo no funcional.

## Estructura del repositorio

Monorepo con dos aplicaciones frontend independientes, sin backend real (datos mock, navegación funcional entre pantallas):

- **[`web/`](web/README.md)** - Aplicación Angular (Material).
- **[`mobile/`](mobile/README.md)** - Aplicación Ionic + Angular + Capacitor.

Cada carpeta tiene su propio `README.md` con el detalle completo de arquitectura y decisiones de diseño. Este documento resume qué se implementó en cada una y cómo correrlas.

## Requisito común: versión de Node

Ambos proyectos usan **Angular 22**, que requiere **Node `^22.22.3 || ^24.15.0 || >=26.0.0`**. Si `node --version` te da algo menor a `24.15.0` en la rama 24.x (por ejemplo `24.14.x`), instala una versión más reciente (`nvm install 24.15.0` o superior) antes de correr `npm install` / `ng serve`, o los comandos de Angular CLI fallarán al iniciar.

---

## Web (`web/`)

Angular 22 standalone + Angular Material, tokens de diseño en `web/src/styles/` (extraídos de Figma), fuente Comfortaa.

### Pantallas implementadas

| Ruta | Pantalla |
| --- | --- |
| `/login` | Inicio de sesión (ruta raíz) |
| `/perfil` | Perfil |
| `/dashboard` | Dashboard |
| `/alarma/:id` | Detalle de alarma |
| `/alarma/:id/vivo` | Detalle de alarma en vivo (sonando) |
| `/reto-escritura` | Reto de escritura para apagar la alarma (con validación en vivo) |
| `/reto-completado` | Reto completado con éxito |
| `/PERFIL` | Perfil de usuario |

Flujo completo navegable con clics, sin editar la URL: `/login` → (Continuar con Google/Apple) `/dashboard` → (Ver detalle) `/alarma/:id` → (Simular: la alarma está sonando) `/alarma/:id/vivo` → (Ir al reto) `/reto-escritura` → (al completar la frase) `/reto-completado` → (Ir al dashboard) `/dashboard`.

### Cómo correrla

```bash
cd web
npm install
npm start          # equivalente a: ng serve
```

Abre `http://localhost:4200/`.

### Tests

```bash
cd web
npm test            # ng test (Vitest)
```

Ver detalle completo en [`web/README.md`](web/README.md).

---

## Mobile (`mobile/`)

Ionic 9 + Angular 22 (standalone) + Capacitor 8, tokens de diseño en `mobile/src/theme/design-tokens.scss`, fuente Comfortaa.

### Pantallas implementadas

| Ruta | Pantalla |
| --- | --- |
| `/alarmas-lista` | Lista de alarmas ya poblada (ruta raíz) |
| `/nueva` | Crear alarma · paso 1/3 (hora, días, etiqueta) |
| `/snooze` | Crear alarma · paso 2/3 (duración del reto, límite de posposiciones) |
| `/reto-config` | Crear alarma · paso 3/3 (pasos a caminar) |
| `/reto-curso` | Reto activo (caminando) |
| `/reto-faltan` | Aviso de pasos faltantes |
| `/reto-ok` | Reto completado |

Flujo completo navegable con clics: `/alarmas-lista` → (`+`) `/nueva` → (Continuar) `/snooze` → (Continuar) `/reto-config` → (Guardar) vuelve a `/alarmas-lista`. También, desde la lista, "Simular: alarma sonando" → `/reto-curso`; y desde los retos activos, el botón de volver/cerrar regresa a `/alarmas-lista`.

### Cómo correrla

```bash
cd mobile
npm install
npm start -- --port 4300   # ng serve; puerto distinto al de web si corres ambas a la vez
```

Abre `http://localhost:4300/` (o `http://localhost:4200/` si la corres sola, sin el flag de puerto).

### Tests

```bash
cd mobile
npm test             # ng test (Vitest)
```

Ver detalle completo en [`mobile/README.md`](mobile/README.md).

---

## Diseño

- Fuente: [Comfortaa](https://fonts.google.com/specimen/Comfortaa) (Google Fonts).
- Mockups de Figma: `snoozeless - mockups - web` y `snoozeless - mockups - mobile`.
