# WBS — Frontend Vite (JS) · CS-005 Catálogo de Películas

> **Para el agente de programación:** este documento es la especificación del frontend. Implementa los paquetes de trabajo **en orden**, respeta las **restricciones** y valida cada uno con su **criterio de aceptación** antes de pasar al siguiente. No agregues funcionalidades que no estén aquí.

---

## 0. Contexto

| Elemento | Valor |
|---|---|
| Repositorio | `https://github.com/CrazyBread7364/-Caso-de-estudio-catalogo-de-peliculas.git` |
| Rama base | `development` |
| Rama de trabajo | `feat/frontend` → PR hacia `development` |
| Backend | Django + DRF en `api/` (puerto 8000), CORS permitido para `http://localhost:5173` |
| Frontend | Vite + JavaScript vanilla en `frontend/` (puerto 5173) |
| Alcance del caso | **Solo registrar y listar películas.** Sin editar, sin borrar, sin buscar, sin login. |
| Evaluación | Lista de cotejo de coevaluación (8 criterios) + demostración en vivo |

### Contrato de la API (verificado contra el backend real)

| Operación | Petición | Respuesta OK | Respuesta error |
|---|---|---|---|
| Listar | `GET /api/v1/movies/` | `200` → `[{ "id", "title", "director", "genre", "duration_minutes" }]` | — |
| Registrar | `POST /api/v1/movies/` con `Content-Type: application/json` | `201` → la película creada (con `id`) | `400` → `{ "campo": ["mensaje", ...], ... }` |

**Reglas del contrato:**
- La URL **siempre lleva barra final** (`/movies/`). Un `POST` sin barra responde **500** (Django `APPEND_SLASH` no puede redirigir un POST).
- `duration_minutes` se envía como **número**, no como texto.
- No enviar `id` en el POST; lo asigna la base de datos.
- Límites del modelo: `title` 200, `director` 200, `genre` 100 caracteres.

### Restricciones (no negociables)

1. **Sin frameworks** (nada de React, Vue, etc.) ni librerías extra: solo Vite + JS vanilla.
2. **Nunca usar `innerHTML`** (ni `insertAdjacentHTML`, ni template strings inyectados como HTML) con datos que vengan del usuario o de la API. Usar `textContent` / `createElement`. (Prevención de XSS.)
3. **Solo `src/api/movieApi.js` puede usar `fetch`.** Los componentes no conocen URLs.
4. **Ningún secreto en variables `VITE_*`**: terminan públicas dentro del bundle.
5. No modificar el backend dentro de esta rama (salvo el paquete 1.0, si el equipo lo decide ahí).

---

## Árbol WBS

```
1. Frontend CS-005
├── 1.0 Prerrequisitos del backend (bloqueantes)
│   ├── 1.0.1 Corregir models.CharField
│   ├── 1.0.2 Generar y aplicar migraciones
│   └── 1.0.3 Restaurar .env en .gitignore
├── 1.1 Preparación del entorno
│   ├── 1.1.1 Crear rama feat/frontend
│   ├── 1.1.2 Generar proyecto Vite (vanilla)
│   ├── 1.1.3 Limpiar plantilla
│   └── 1.1.4 Variables de entorno (.env / .env.example)
├── 1.2 Capa de datos (api)
│   └── 1.2.1 src/api/movieApi.js
├── 1.3 Capa de presentación (components)
│   ├── 1.3.1 index.html (estructura)
│   ├── 1.3.2 src/components/movieForm.js
│   ├── 1.3.3 src/components/movieTable.js
│   └── 1.3.4 src/components/message.js
├── 1.4 Orquestación
│   └── 1.4.1 src/main.js
├── 1.5 Estilos
│   └── 1.5.1 src/style.css
├── 1.6 Pruebas
│   ├── 1.6.1 Prueba funcional (flujo feliz)
│   ├── 1.6.2 Pruebas de error
│   └── 1.6.3 Prueba de seguridad (XSS)
└── 1.7 Cierre
    ├── 1.7.1 README (cómo ejecutar)
    ├── 1.7.2 Commits + PR a development
    └── 1.7.3 Guion de demostración
```

---

## 1.0 Prerrequisitos del backend (bloqueantes)

> Sin esto el front no tiene contra qué probar. Idealmente en una rama aparte `fix/backend` → `development`.

### 1.0.1 Corregir `models.CharField`
- **Archivo:** `api/MovieService/models.py`
- **Cómo:** cambiar `models.charfield(max_length = 200)` → `models.CharField(max_length=200)`.
- **Aceptación:** `python manage.py check` no muestra errores.

### 1.0.2 Generar y aplicar migraciones
- **Cómo:**
  ```bash
  cd api
  python manage.py makemigrations MovieService
  python manage.py migrate
  ```
- **Aceptación:** existe `api/MovieService/migrations/0001_initial.py` y `GET http://localhost:8000/api/v1/movies/` responde `200` con `[]`.

### 1.0.3 Restaurar `.env` en `.gitignore`
- **Archivo:** `.gitignore` (raíz). Agregar la línea `.env` en la sección `# Environments`.
- **Recomendado:** mover `SECRET_KEY` y `PASSWORD` de `settings.py` a variables de entorno.
- **Aceptación:** `git status` no muestra archivos `.env`.

---

## 1.1 Preparación del entorno

### 1.1.1 Crear rama
```bash
git checkout development && git pull
git checkout -b feat/frontend
```
- **Aceptación:** `git branch` muestra `* feat/frontend`.

### 1.1.2 Generar proyecto Vite
- **Cómo (desde la raíz del repo):**
  ```bash
  npm create vite@latest frontend -- --template vanilla
  cd frontend
  npm install
  ```
- **Aceptación:** `npm run dev` levanta en `http://localhost:5173`.

### 1.1.3 Limpiar plantilla
- **Cómo:** borrar `src/counter.js`, `src/javascript.svg`, `public/vite.svg`; vaciar `src/main.js` y `src/style.css`; quitar referencias en `index.html`.
- **Aceptación:** la página carga en blanco sin errores en consola.

### 1.1.4 Variables de entorno
- **Archivos:**
  - `frontend/.env.example` (se sube a git):
    ```
    VITE_API_URL=http://localhost:8000/api/v1
    ```
  - `frontend/.env` (copia local, **no** se sube).
- **Cómo:** asegurar que `frontend/.gitignore` incluya `.env` y `node_modules`.
- **Aceptación:** `import.meta.env.VITE_API_URL` imprime la URL en consola.

**Estructura final esperada:**
```
frontend/
├── index.html
├── .env.example
├── package.json
└── src/
    ├── main.js
    ├── style.css
    ├── api/
    │   └── movieApi.js
    └── components/
        ├── movieForm.js
        ├── movieTable.js
        └── message.js
```

---

## 1.2 Capa de datos

### 1.2.1 `src/api/movieApi.js`
- **Responsabilidad:** única pieza que habla con el backend. Exporta `getMovies()` y `createMovie(movie)`.
- **Cómo:**
  - `BASE_URL = \`${import.meta.env.VITE_API_URL}/movies/\`` (con barra final).
  - `getMovies()`: `fetch(BASE_URL)`; si `!res.ok` lanza `Error`; devuelve `res.json()`.
  - `createMovie(movie)`: `POST` con `headers: {'Content-Type': 'application/json'}` y `body: JSON.stringify(movie)`. Si `!res.ok`, convertir la respuesta de DRF a texto legible y lanzar `Error`.
  - Manejar fallo de red (backend apagado): capturar el error de `fetch` y lanzar un mensaje claro (“No se pudo conectar con el servidor”).
- **Referencia:**
  ```js
  const BASE_URL = `${import.meta.env.VITE_API_URL}/movies/`;

  function parseErrors(data) {
    // DRF: { campo: ["mensaje", ...] }
    return Object.entries(data)
      .map(([field, msgs]) => `${field}: ${[].concat(msgs).join(', ')}`)
      .join(' | ');
  }

  async function request(url, options) {
    try {
      return await fetch(url, options);
    } catch {
      throw new Error('No se pudo conectar con el servidor.');
    }
  }

  export async function getMovies() {
    const res = await request(BASE_URL);
    if (!res.ok) throw new Error('No se pudo cargar el catálogo.');
    return res.json();
  }

  export async function createMovie(movie) {
    const res = await request(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(movie),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(parseErrors(data));
    return data;
  }
  ```
- **Aceptación:** desde la consola del navegador, `getMovies()` devuelve el arreglo y `createMovie({...})` devuelve el objeto con `id`.

---

## 1.3 Capa de presentación

### 1.3.1 `index.html`
- **Contenido:**
  - `<h1>` Catálogo de Películas.
  - `<form id="movie-form" novalidate>` con 4 campos, cada uno con `<label>`:
    | name | type | atributos |
    |---|---|---|
    | `title` | text | `required maxlength="200"` |
    | `director` | text | `required maxlength="200"` |
    | `genre` | text | `required maxlength="100"` |
    | `duration_minutes` | number | `required min="1" step="1"` |
  - Botón `type="submit"` “Registrar”.
  - `<p id="message" role="status" aria-live="polite">` para mensajes.
  - `<table>` con `<thead>` (ID, Título, Director, Género, Duración (min)) y `<tbody id="movie-list">`.
  - `<script type="module" src="/src/main.js">`.
- **Aceptación:** la página muestra formulario y tabla vacía, sin errores.

### 1.3.2 `src/components/movieForm.js`
- **Responsabilidad:** leer y reiniciar el formulario. No llama a la API.
- **Exporta:**
  - `readMovieForm(form)` → `{ title, director, genre, duration_minutes }`, con `trim()` en textos y `Number()` en la duración.
  - `resetMovieForm(form)` → `form.reset()` y foco en el primer campo.
  - `setFormDisabled(form, disabled)` → deshabilita el botón mientras se envía (evita registros dobles).
- **Aceptación:** `readMovieForm` devuelve `duration_minutes` como `number`.

### 1.3.3 `src/components/movieTable.js`
- **Responsabilidad:** dibujar la lista.
- **Exporta:** `renderMovieTable(tbody, movies)`.
- **Cómo:**
  - `tbody.replaceChildren()` para limpiar.
  - Si `movies.length === 0`: una fila con celda `colSpan = 5` y texto “Aún no hay películas registradas.”.
  - Por cada película: `tbody.insertRow()` y `row.insertCell().textContent = valor` para `id, title, director, genre, duration_minutes`.
  - **Prohibido `innerHTML`.**
- **Aceptación:** con 3 películas se dibujan 3 filas en el orden recibido.

### 1.3.4 `src/components/message.js`
- **Exporta:** `showMessage(el, text, type)` donde `type` es `'success' | 'error'`. Usa `textContent` y asigna la clase CSS.
- **Aceptación:** el mensaje cambia de color según el tipo.

---

## 1.4 Orquestación

### 1.4.1 `src/main.js`
- **Responsabilidad:** conectar las piezas; sin lógica de negocio ni `fetch` directo.
- **Flujo:**
  1. Importar `./style.css`, la API y los componentes.
  2. `loadMovies()`: `getMovies()` → `renderMovieTable()`; si falla → `showMessage(..., 'error')`.
  3. Listener `submit` del formulario:
     1. `event.preventDefault()`.
     2. `setFormDisabled(form, true)`.
     3. `movie = readMovieForm(form)`.
     4. `created = await createMovie(movie)`.
     5. `showMessage("Película \"<title>\" registrada con ID <id>.", 'success')`.
     6. `resetMovieForm(form)` y `await loadMovies()`.
     7. En `catch`: `showMessage(err.message, 'error')` (no limpiar el formulario).
     8. En `finally`: `setFormDisabled(form, false)`.
  4. Llamar `loadMovies()` al iniciar.
- **Aceptación:** registrar una película actualiza la tabla sin recargar la página.

---

## 1.5 Estilos

### 1.5.1 `src/style.css`
- **Alcance mínimo** (no invertir tiempo de más, la actividad es de 4 horas):
  - Contenedor centrado (`max-width: ~860px`).
  - Formulario en rejilla de 2 columnas; 1 columna en pantallas `< 600px`.
  - Tabla con bordes suaves y encabezado resaltado.
  - Clases `.success` (verde) y `.error` (rojo).
  - Botón deshabilitado visualmente distinto.
- **Aceptación:** se ve ordenado en escritorio y en celular (DevTools → modo responsive).

---

## 1.6 Pruebas

> Con backend (`python manage.py runserver`) y frontend (`npm run dev`) corriendo.

### 1.6.1 Flujo feliz
| # | Acción | Resultado esperado |
|---|---|---|
| 1 | Abrir `http://localhost:5173` | Tabla carga (vacía o con datos) |
| 2 | Registrar “Inception / Christopher Nolan / Ciencia ficción / 148” | Mensaje verde con ID |
| 3 | Revisar la tabla | La película aparece sin recargar |
| 4 | Recargar la página (F5) | La película sigue ahí (persistió en Postgres) |

### 1.6.2 Errores
| # | Acción | Resultado esperado |
|---|---|---|
| 1 | Enviar formulario vacío | Mensaje rojo con errores de DRF por campo |
| 2 | Apagar Django y recargar | Mensaje “No se pudo conectar con el servidor.” |
| 3 | Clic rápido doble en “Registrar” | Solo se crea un registro (botón deshabilitado) |

### 1.6.3 Seguridad (XSS)
| # | Acción | Resultado esperado |
|---|---|---|
| 1 | Registrar título `<img src=x onerror=alert(1)>` | Aparece como **texto** en la tabla; **no** sale ningún `alert` |

- **Aceptación del paquete:** todas las filas anteriores pasan; consola del navegador sin errores.

---

## 1.7 Cierre

### 1.7.1 README
Agregar a `README.md` de la raíz una sección “Cómo ejecutar”:
1. Backend: crear venv, `pip install -r requirements.txt`, configurar BD, `migrate`, `runserver`.
2. Frontend: `cd frontend`, `cp .env.example .env`, `npm install`, `npm run dev`.

### 1.7.2 Commits y PR
- Commits pequeños con el mismo estilo del repo (conventional commits), p. ej.:
  - `chore: scaffold vite frontend`
  - `feat: movie api client`
  - `feat: movie form and table components`
  - `feat: wire main.js`
  - `style: base styles`
  - `docs: run instructions`
- Abrir PR `feat/frontend` → `development` y que otro integrante lo revise.

### 1.7.3 Guion de demostración (≈3 min)
1. Mostrar estructura de carpetas: back (`models → services → views`) y front (`api → components → main`). *(Criterio 4)*
2. Levantar ambos servidores. *(Criterio 2)*
3. Registrar una película. *(Criterio 5)*
4. Mostrar la tabla y recargar para probar persistencia. *(Criterios 6 y 7)*
5. Señalar que los campos son exactamente los del caso. *(Criterios 1, 3 y 8)*

---

## Trazabilidad con la lista de cotejo

| # | Criterio | Paquete(s) que lo cubren |
|---|---|---|
| 1 | Corresponde al caso asignado | 0 (alcance), 1.3.1 |
| 2 | Se ejecuta en el entorno de desarrollo | 1.0, 1.1, 1.7.1 |
| 3 | Usa los datos del caso | 1.3.1, 1.3.3 |
| 4 | Organización básica de componentes | 1.1.4 (estructura), 1.2, 1.3, 1.4 |
| 5 | Permite registrar | 1.2.1, 1.3.2, 1.4.1 |
| 6 | Permite consultar/listar | 1.2.1, 1.3.3, 1.4.1 |
| 7 | Demostración de operaciones | 1.6, 1.7.3 |
| 8 | Cumple requerimientos básicos | Todo el WBS + restricciones |

## Definición de terminado (DoD)

- [ ] Backend arranca y responde en `/api/v1/movies/`.
- [ ] Front registra y lista contra el backend real.
- [ ] Ningún `innerHTML` con datos dinámicos (`grep -r innerHTML frontend/src` vacío).
- [ ] Solo `movieApi.js` contiene `fetch`.
- [ ] `.env` fuera de git (back y front).
- [ ] Todas las pruebas de 1.6 pasan.
- [ ] PR revisado y fusionado en `development`.
