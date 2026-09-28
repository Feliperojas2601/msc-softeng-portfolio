# Design Tokens — Referencia (snoozeless Web)

Fuente: archivo de Figma **"snoozeless - mockups - web"**
([enlace](https://www.figma.com/design/dlNlMlowd1u96uNKAq91fk/snoozeless---mockups---web))

Todos los valores de este documento y de `design-tokens.scss` se extrajeron
directamente del archivo de Figma vía el Figma MCP (Plugin API) — Variables
de color y Text Styles locales del archivo. Ningún valor fue inventado ni
aproximado.

> **Nota:** al momento de la extracción, el archivo ya no contiene los 10
> Text Styles originales del wireframe en escala de grises (Display, Título
> de pantalla, Título de sección, Subtítulo, Cuerpo, Cuerpo de lectura, Label
> de campo, Label de botón, aviso, Valor de campo) — parecen haber sido
> eliminados en algún momento después de la migración inicial. Esta
> referencia documenta únicamente lo que existe actualmente en el archivo.

---

## 1. Color — Tokens primitivos

Colección de Variables de Figma: **"Color"**, modo **"Default"**.

| Token SCSS | Nombre en Figma | Hex | Propósito |
|---|---|---|---|
| `$color-papel` | Papel | `#FAF6F0` | Blanco cálido de la marca; fondo base de pantallas y barras. |
| `$color-papel-2` | Papel 2 | `#F3EEE4` | Variante ligeramente más oscura de Papel; usada en tarjetas y superficies elevadas sobre el fondo base. |
| `$color-papel-3` | Papel 3 | `#ECE4D7` | Tercer tono de la familia Papel, para superficies aún más diferenciadas (p. ej. banners informativos). |
| `$color-tinta` | Tinta | `#2B2A26` | Negro cálido; color de texto principal y fondo en pantallas de tema oscuro. |
| `$color-tinta-80` | Tinta 80 | `#615F58` | Tinta aclarada; superficies sobre fondo oscuro (p. ej. tarjetas dentro de un modal oscuro) y texto secundario. |
| `$color-amanecer` | Amanecer | `#E68A3E` | Naranja de marca (color de acento primario); botones primarios, elementos activos, iconografía destacada. |
| `$color-amanecer-oscuro` | Amanecer oscuro | `#B4651F` | Variante oscura de Amanecer; texto/iconos sobre fondos claros de acento, estados "fuerte" del acento. |
| `$color-amanecer-soft` | Amanecer soft | `#F7E3CE` | Variante muy clara de Amanecer; fondos de resaltado suave (p. ej. ítem de navegación seleccionado). |
| `$color-amanecer-tint` | Amanecer tint | `#F4CB9F` | Tinte intermedio de Amanecer; usos decorativos o de énfasis medio. |
| `$color-bruma` | Bruma | `#D9CFC0` | Beige neutro; bordes, divisores y superficies de "pista" (tracks) en controles. |
| `$color-bruma-oscuro` | Bruma oscuro | `#B3A78E` | Bruma oscurecida; bordes con más contraste, texto terciario/deshabilitado. |
| `$color-salvia` | Salvia | `#6E9C7E` | Verde de marca; estados de éxito/positivos, indicadores "en vivo". |
| `$color-salvia-oscuro` | Salvia oscuro | `#4F7359` | Variante oscura de Salvia; texto sobre fondos claros de éxito. |
| `$color-salvia-tint` | Salvia tint | `#C6D8CC` | Variante muy clara de Salvia; fondos suaves de éxito (banners, leyendas). |
| `$color-texto-atenuado` | Texto atenuado | `#75736C` | Gris cálido neutro; texto secundario/atenuado sobre fondos claros. |
| `$color-terracota` | Terracota | `#C0523F` | Rojo-terracota; color de peligro/error/alerta. |
| `$color-terracota-suave` | Terracota suave | `#F3DBD4` | Variante muy clara de Terracota; fondos suaves de peligro/alerta. |

## 2. Color — Tokens semánticos (`sem/*`)

Cada uno es un **alias de Variable** en Figma: no tiene un valor propio, sino
que apunta a uno de los tokens primitivos de la tabla anterior. En el SCSS,
cada variable semántica referencia directamente la variable primitiva
correspondiente (no se duplica el valor hexadecimal), preservando la misma
relación de alias que existe en Figma.

| Token SCSS | Nombre en Figma | Apunta a | Scope en Figma | Propósito |
|---|---|---|---|---|
| `$color-sem-fondo` | sem/Fondo | Papel | Fondo de frame/forma | Fondo base de pantalla. |
| `$color-sem-superficie` | sem/Superficie | Papel 2 | Fondo de frame/forma | Superficie elevada estándar (tarjetas). |
| `$color-sem-superficie-alta` | sem/Superficie alta | Papel 3 | Fondo de frame/forma | Superficie con mayor elevación/diferenciación. |
| `$color-sem-borde` | sem/Borde | Bruma | Color de borde | Borde por defecto de tarjetas, campos, divisores. |
| `$color-sem-borde-fuerte` | sem/Borde fuerte | Bruma oscuro | Color de borde | Borde con más énfasis/contraste. |
| `$color-sem-texto` | sem/Texto | Tinta | Color de texto | Texto principal. |
| `$color-sem-texto-secundario` | sem/Texto secundario | Tinta 80 | Color de texto | Texto secundario. |
| `$color-sem-texto-atenuado` | sem/Texto atenuado | Texto atenuado | Color de texto | Texto terciario/atenuado. |
| `$color-sem-acento` | sem/Acento | Amanecer | Fondo, texto, borde | Acento de marca por defecto. |
| `$color-sem-acento-fuerte` | sem/Acento fuerte | Amanecer oscuro | Fondo, texto | Acento en su variante de mayor contraste. |
| `$color-sem-acento-suave` | sem/Acento suave | Amanecer soft | Fondo de frame/forma | Acento en fondo suave (resaltados). |
| `$color-sem-exito` | sem/Éxito | Salvia | Fondo, texto | Estado de éxito/confirmación. |
| `$color-sem-exito-suave` | sem/Éxito suave | Salvia tint | Fondo de frame/forma | Fondo suave para estado de éxito. |
| `$color-sem-peligro` | sem/Peligro | Terracota | Fondo, texto | Estado de error/peligro/alerta. |
| `$color-sem-peligro-suave` | sem/Peligro suave | Terracota suave | Fondo de frame/forma | Fondo suave para estado de peligro. |

## 3. Tipografía

Todos los Text Styles del archivo usan la familia **Comfortaa**
(`$font-family-base`). Cada estilo se documenta con su peso, tamaño,
interlineado y tracking exactos, tal como los reporta Figma.

### 3.1 Escala "Web/*" (oficial)

Esta es la escala tipográfica oficial del proyecto. El archivo de Figma
también contenía una escala anterior sin el prefijo `Web/` (N1 · Título
pantalla, N2 · Sección, N3 · Campo, Mockup · Subtítulo, Mockup · Cuerpo,
Cuerpo S, Etiqueta, Botón, Destacado, Reloj) — esa escala viene de una
referencia de mobile que no aplica a este proyecto, así que se excluyó
deliberadamente tanto de este documento como de `design-tokens.scss`.

| Token base | Nombre en Figma | Peso | Tamaño | Interlineado | Tracking | Propósito (inferido del nombre) |
|---|---|---|---|---|---|---|
| `web-display` | Web/Display | 700 (Bold) | 40px | 48px | 0px | Texto de mayor jerarquía visual (portadas, hitos). |
| `web-titulo-pagina` | Web/Título de página | 700 (Bold) | 30px | 38px | 0px | Título de una página completa. |
| `web-titulo-seccion` | Web/Título de sección | 600 (SemiBold) | 20px | 28px | 0px | Encabezado de sección. |
| `web-subtitulo` | Web/Subtítulo | 500 (Medium) | 16px | 24px | 0px | Subtítulo de apoyo. |
| `web-cuerpo` | Web/Cuerpo | 400 (Regular) | 15px | 24px | 0px | Texto de cuerpo estándar. |
| `web-cuerpo-s` | Web/Cuerpo S | 400 (Regular) | 13px | 20px | 0px | Texto de cuerpo pequeño. |
| `web-etiqueta` | Web/Etiqueta | 500 (Medium) | 12px | 16px | 0.6px | Etiquetas; único estilo con tracking positivo (mayor separación entre letras, típico de etiquetas en mayúsculas). |
| `web-boton` | Web/Botón | 600 (SemiBold) | 15px | 20px | 0px | Texto de botones. |
| `web-dato` | Web/Dato | 700 (Bold) | 34px | 40px | 0px | Cifras/datos destacados (p. ej. métricas de un dashboard). |
| `web-reloj` | Web/Reloj | 500 (Medium) | 56px | 64px | 0px | Display numérico grande (p. ej. la hora de una alarma). |

---

## Cómo se generó este documento

1. Se listaron las colecciones de Variables locales del archivo de Figma
   (`figma.variables.getLocalVariableCollectionsAsync()`) y se leyó cada
   variable con su valor exacto por modo, incluyendo la resolución de los
   alias (`VARIABLE_ALIAS`) a su variable primitiva de origen.
2. Se listaron los Text Styles locales del archivo
   (`figma.getLocalTextStylesAsync()`) con familia, peso, tamaño,
   interlineado y tracking exactos.
3. Ninguna variable tenía una descripción (`description`) escrita en Figma;
   el campo "Propósito" de cada tabla es una inferencia razonable a partir
   del nombre semántico y el *scope* de uso reportado por Figma (fondo,
   texto o borde), no un valor extraído — los valores numéricos y hex sí son
   exactos y provienen directamente del MCP.
