# Backend - PatchProof MVP

Este directorio contiene la API REST (FastAPI) y la capa de base de datos relacional (SQLite + SQLAlchemy) para el MVP de PatchProof.

## Estructura de la Base de Datos

En lugar de utilizar scripts DDL o un motor externo pesado, el MVP utiliza SQLite con un ORM (SQLAlchemy) para agilizar el desarrollo y las pruebas locales. La arquitectura de datos se divide en tres archivos principales:

*   **`database.py` (Conexión y Motor):** 
    Configura la comunicación física con SQLite. Provee la dependencia `get_db()`, una fábrica de sesiones que abre una transacción temporal para cada petición de la API y la cierra automáticamente, evitando bloqueos en la base de datos.
*   **`models.py` (Esquema de Datos):** 
    Mapea el modelo relacional a clases de Python. Define las tablas `bounties` y `reports`. Sirve como el diccionario de datos principal del equipo; cualquier cambio estructural en las entidades debe reflejarse primero aquí.
*   **`init_db.py` (Script de Inicialización):** 
    Script de ejecución única. Al correrlo, lee las clases de `models.py` y ejecuta las sentencias `CREATE TABLE` nativas para generar físicamente el archivo `patchproof_mvp.db` en tu máquina local.

## Guía de Inicio Rápido

Para levantar el entorno de base de datos en tu máquina local:

1. Asegúrate de tener el entorno virtual activado (`source venv/Scripts/activate` en Windows/Git Bash).
2. Instala las dependencias: `pip install -r requirements.txt`
3. Genera la base de datos local: `python init_db.py`
4. (Opcional) Verifica que el archivo `patchproof_mvp.db` se haya creado en la raíz de esta carpeta.