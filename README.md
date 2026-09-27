# Caso de Estudio: Catálogo de Películas (CS-005)

**Actividad 1:** Programa informático de implementación de un entorno de desarrollo de aplicaciones web progresivas.

Aplicación web que permite **registrar** películas y **consultar el catálogo** completo, implementada con separación en capas.

---

## Alcance

Conforme al caso de estudio CS-005, el programa maneja únicamente los datos y operaciones solicitados:

| Datos de `Movie` | Operaciones |
|---|---|
| `id`, `title`, `director`, `genre`, `duration_minutes` | Insertar (registrar) y listar |

No se incorporan campos ni funcionalidades adicionales.

---

## Arquitectura en Capas

| Capa | Ubicación | Responsabilidad |
|---|---|---|
| **Persistencia** | `api/MovieService/models.py`, `migrations/` | Entidad `Movie` mapeada a la tabla `MovieService_movie` en PostgreSQL |
| **Negocio** | `api/MovieService/services.py` | Clase `MovieServices`: encapsula el guardado y la recuperación |
| **Presentación** | `api/MovieService/views.py` + `frontend/` | API REST (puerto `8000`) y cliente web Vite (puerto `5173`) |

---

## Requisitos Previos

| Herramienta | Versión | Probado con |
|---|---|---|
| Python | 3.10+ | 3.14 y 3.12 |
| Node.js y npm | 18+ | Node 24 / npm 11 |
| PostgreSQL | 12+ | 18.6 (puerto `5432`) |
| Git | — | — |

---

## 1. Configuración de la Base de Datos (PostgreSQL)

El proyecto utiliza una base de datos llamada `caescapel`. El respaldo incluye **10 películas de ejemplo** ya cargadas.

### Opción A — script automatizado (recomendado)

Desde la raíz del proyecto:

```bash
python setup_db.py
```

En Windows también está disponible la versión PowerShell:

```bash
.\setup_db.ps1
```

El script localiza `psql` automáticamente (incluso si no está en el `PATH`), crea la base si no existe, restaura el respaldo y valida el número de películas cargadas.

Credenciales por defecto (sobrescribibles con las variables de entorno `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`):

```
base: caescapel   usuario: postgres   contraseña: root   host: localhost   puerto: 5432
```

### Opción B — manual

1. **Crear la base de datos vacía:**
   ```bash
   psql -U postgres -d postgres -c "CREATE DATABASE caescapel;"
   ```

2. **Restaurar las tablas y datos:**
   ```bash
   psql -U postgres -d caescapel -f backup_completo_caescapel.sql
   ```

> **Nota (Windows):** el instalador de PostgreSQL no agrega `psql` al `PATH`. Si el comando no se reconoce, usa la ruta completa, por ejemplo:
> `"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres ...`

---

## 2. Puesta en Marcha del Backend (Django)

1. **Navegar al directorio del backend:**
   ```bash
   cd api
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   # En Windows (PowerShell):
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # En Linux / macOS:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Verificar la configuración de la base de datos:**
   Revisar el bloque `DATABASES` en `api/config/settings.py` y ajustarlo si tus credenciales de PostgreSQL son distintas a las de arriba.

5. **Aplicar migraciones:**
   ```bash
   python manage.py migrate
   ```
   *Si restauraste el respaldo, Django responderá `No migrations to apply`: el esquema ya está en su lugar.*

6. **Iniciar el servidor de desarrollo:**
   ```bash
   python manage.py runserver 8000
   ```
   La API queda disponible en `http://localhost:8000/api/v1/movies/`.

---

## 3. Puesta en Marcha del Frontend (Vite)

1. **Navegar al directorio del frontend** (en otra terminal, dejando Django corriendo):
   ```bash
   cd frontend
   ```

2. **Configurar variables de entorno:**
   ```bash
   # En Windows (PowerShell):
   Copy-Item .env.example .env

   # En Linux / macOS:
   cp .env.example .env
   ```
   *Por defecto apunta a `VITE_API_URL=http://localhost:8000/api/v1`.*

3. **Instalar dependencias de Node:**
   ```bash
   npm install
   ```

4. **Iniciar el servidor de desarrollo:**
   ```bash
   npm run dev
   ```
   La aplicación queda disponible en `http://localhost:5173`.

> El backend acepta peticiones desde `http://localhost:5173` (ver `CORS_ALLOWED_ORIGINS` en `settings.py`). Si Vite arranca en otro puerto, hay que agregarlo ahí.

---

## API

Base: `http://localhost:8000/api/v1`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/movies/` | Lista todas las películas |
| `POST` | `/movies/` | Registra una película nueva |

**Ejemplo de registro:**

```bash
curl -X POST http://localhost:8000/api/v1/movies/ -H "Content-Type: application/json" -d "{\"title\":\"Coco\",\"director\":\"Lee Unkrich\",\"genre\":\"Animacion\",\"duration_minutes\":105}"
```

Respuesta `201 Created`:

```json
{"id":12,"title":"Coco","director":"Lee Unkrich","genre":"Animación","duration_minutes":105}
```

Los datos incompletos o inválidos devuelven `400 Bad Request` con el detalle por campo.

---

## Verificación del Funcionamiento

1. Abrir `http://localhost:5173`: la tabla muestra las películas ya registradas.
2. Llenar el formulario y pulsar **Registrar**: aparece un mensaje de confirmación con el ID asignado.
3. La tabla se recarga automáticamente e incluye la nueva película.
4. Comprobar la persistencia directamente en la base de datos:
   ```bash
   psql -U postgres -d caescapel -c "SELECT * FROM \"MovieService_movie\" ORDER BY id;"
   ```

---

## Estructura del Proyecto

```
.
├── api/                                # Backend Django + DRF
│   ├── config/
│   │   ├── settings.py                 # Configuración, DB y CORS
│   │   └── urls.py                     # Ruteo raíz (/api/v1/)
│   ├── MovieService/
│   │   ├── models.py                   # [Persistencia] Entidad Movie
│   │   ├── migrations/0001_initial.py  # [Persistencia] Esquema de la tabla
│   │   ├── services.py                 # [Negocio] MovieServices
│   │   ├── serializers.py              # Validación y (de)serialización
│   │   ├── views.py                    # [Presentación] MovieListView
│   │   └── urls.py                     # Endpoint /movies/
│   └── manage.py
├── frontend/                           # Cliente web Vite + JavaScript
│   ├── index.html                      # Marcado semántico y accesible
│   ├── .env.example                    # Plantilla de variables públicas
│   └── src/
│       ├── main.js                     # Orquestación de eventos y ciclo de vida
│       ├── style.css                   # Estilos responsivos con CSS Grid/Flexbox
│       ├── api/movieApi.js             # Cliente HTTP centralizado (único uso de fetch)
│       └── components/
│           ├── movieForm.js            # Lectura y estado del formulario
│           ├── movieTable.js           # Renderizado seguro del DOM
│           └── message.js              # Feedback visual de éxito/error
├── backup_completo_caescapel.sql       # Respaldo de la base con datos de ejemplo
├── setup_db.py / setup_db.ps1          # Automatización de creación y restauración
└── requirements.txt                    # Dependencias de Python
```

---

## Criterios de Seguridad Aplicados

* **Mitigación XSS:** cero uso de `innerHTML` o inyección de cadenas en el DOM. Todo el renderizado dinámico se realiza mediante `textContent`, `createElement` y `replaceChildren`.
* **Manejo de estados:** deshabilitación automática del botón de registro durante peticiones asíncronas para prevenir registros duplicados.
* **Segregación de secretos:** los archivos `.env` están excluidos del control de versiones vía `.gitignore`.
* **CORS restringido:** solo se permite el origen del frontend de desarrollo.

---

## Ramas

`main` y `development` contienen el proyecto completo e integrado (backend, frontend y base de datos). Las ramas `feat/*` y `Database` corresponden al desarrollo por módulos y ya están fusionadas.
