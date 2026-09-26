# Caso de Estudio: Catálogo de Películas

**Actividad 1:** Programa informático de implementación de un entorno de desarrollo de aplicaciones web progresivas.

---

## Requisitos Previos

Asegúrate de contar con las siguientes herramientas instaladas localmente:
- **Python 3.10+** (probado en Python 3.14)
- **PostgreSQL** en ejecución local (puerto estándar `5432`)
- **Git**

---

## 1. Configuración de la Base de Datos (PostgreSQL)

El proyecto utiliza una base de datos llamada `caescapel`. Para inicializarla junto con todas sus tablas y datos predefinidos:

1. **Crear la base de datos vacía:**
   ```bash
   psql -U postgres -d postgres -c "CREATE DATABASE caescapel;"
