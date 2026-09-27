# Caso de Estudio: Catálogo de Películas

**Actividad 1:** Programa informático de implementación de un entorno de desarrollo de aplicaciones web progresivas.

---

## Arquitectura de la Solución

El proyecto consta de una arquitectura desacoplada en capas:
* **Persistencia:** modelo `Movie` (`id`, `title`, `director`, `genre`, `duration_minutes`) + PostgreSQL.
* **Negocio:** `MovieService/services.py` (`MovieServices`).
* **Presentación:** API REST (`api/`, puerto `8000`, endpoints en `/api/v1/movies/`) y cliente web Vite + JavaScript (`frontend/`, puerto `5173`).

---

## Requisitos Previos

* Python 3.10+ (probado en Python 3.14)
* Node.js 18+ y npm
* PostgreSQL en ejecución local (puerto estándar `5432`)
* Git

---

## 1. Configuración de la Base de Datos (PostgreSQL)

El proyecto utiliza una base de datos llamada `caescapel`.

**Opción A — script automatizado:**
```bash
python setup_db.py
```
(en Windows también está disponible `setup_db.ps1`)

**Opción B — manual:**

1. **Crear la base de datos vacía:**
   ```bash
   psql -U postgres -d postgres -c "CREATE DATABASE caescapel;"
   ```

2. **Restaurar las tablas y datos de la DB:**
   ```bash
   psql -U postgres -d caescapel -f backup_completo_caescapel.sql
   ```

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

4. **Configurar la base de datos:**
   Verificar las credenciales de PostgreSQL en `api/config/settings.py` (por defecto: base `caescapel`, usuario `postgres`, puerto `5432`).

5. **Aplicar migraciones:**
   ```bash
   python manage.py migrate
   ```

6. **Iniciar el servidor de desarrollo de Django:**
   ```bash
   python manage.py runserver 8000
   ```
   La API quedará disponible en `http://localhost:8000/api/v1/movies/`.

---

## 3. Puesta en Marcha del Frontend (Vite)

1. **Navegar al directorio del frontend:**
   ```bash
   cd frontend
   ```

2. **Configurar variables de entorno:**
   Copiar la plantilla de entorno:
   ```bash
   # En Windows (PowerShell):
   Copy-Item .env.example .env

   # En Linux / macOS:
   cp .env.example .env
   ```
   *Nota: Por defecto apunta a `VITE_API_URL=http://localhost:8000/api/v1`.*

3. **Instalar dependencias de Node:**
   ```bash
   npm install
   ```

4. **Iniciar el servidor de desarrollo de Vite:**
   ```bash
   npm run dev
   ```
   La aplicación se abrirá en `http://localhost:5173`.

---

## Estructura del Frontend (`frontend/`)

```
frontend/
├── index.html                  # Marcado semántico y accesible
├── .env.example                # Plantilla de variables de entorno públicas
├── package.json
└── src/
    ├── main.js                 # Orquestación de eventos y ciclo de vida
    ├── style.css               # Estilos responsivos con CSS Grid/Flexbox
    ├── api/
    │   └── movieApi.js         # Cliente HTTP centralizado (único uso de fetch)
    └── components/
        ├── movieForm.js        # Lectura y estado del formulario
        ├── movieTable.js       # Renderizado seguro DOM (sin innerHTML)
        └── message.js          # Feedback visual de éxito/error accesible
```

---

## Verificación y Criterios de Seguridad

* **Mitigación XSS:** Cero uso de `innerHTML` o inyección de cadenas en el DOM. Todo el renderizado dinámico se realiza mediante `textContent`, `createElement` y `replaceChildren`.
* **Manejo de estados:** Deshabilitación automática del botón de registro durante peticiones asíncronas para prevenir registros duplicados.
* **Segregación de secretos:** Archivos `.env` excluidos de control de versiones vía `.gitignore`.
