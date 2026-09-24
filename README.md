# Resumen de Integración y Setup Base
**Autor:** David (Integración / Base de Datos)
**Objetivo:** Establecer la infraestructura base para que Backend, Frontend y Blockchain puedan trabajar en paralelo sin bloqueos.

## 1. Entorno y Dependencias
*   **Carpeta `backend/`:** Contiene toda la lógica del servidor.
*   **`requirements.txt`:** Lista exacta de dependencias instaladas (FastAPI, SQLAlchemy, Uvicorn, Pydantic). 
*   **Acción requerida:** Todos los que toquen el backend deben crear su entorno virtual (`venv`), activarlo y correr `pip install -r requirements.txt`.

## 2. Base de Datos Local (SQLite)
Para evitar la fricción de instalar Docker o motores externos durante el hackathon, utilizamos SQLite con SQLAlchemy.
*   **`backend/database.py`:** Configura el motor y exporta `get_db()`, la función que inyectará la sesión de la base de datos en los endpoints.
*   **`backend/models.py`:** Define la estructura de las tablas `Bounty` y `Report`. Si necesitamos agregar un campo nuevo, se hace aquí.
*   **`backend/init_db.py`:** Script para construir el archivo físico.
*   **Acción requerida:** Cada desarrollador debe correr `python init_db.py` en su máquina para generar su propio archivo `patchproof_mvp.db` (el cual está ignorado en git para evitar conflictos).

## 3. Esqueleto de la API y Frontend
*   **`backend/main.py`:** Punto de entrada de FastAPI. 
*   **CORS Habilitado:** Ya configuré el middleware de CORS permitiendo todos los orígenes (`allow_origins=["*"]`). La **Persona 2 (Frontend)** puede hacer peticiones locales (fetch/axios) desde su proyecto en React hacia `http://localhost:8000` sin recibir bloqueos de seguridad del navegador.

## 4. Lógica Criptográfica (Off-Chain a On-Chain)
*   **`backend/hashing.py`:** Contiene la función `generate_report_hash(report_content, salt)`.
*   **Uso:** Cuando un investigador envíe un reporte, la **Persona 1 (Backend)** utilizará esta función para generar el SHA-256. Este hash será el dato exacto que la **Persona 3 (Blockchain)** enviará al smart contract o transacción de Stellar Testnet.

## 5. Siguientes Pasos Inmediatos
*   **Persona 1 (Backend):** Ya puedes abrir `main.py` y comenzar a programar los endpoints (`POST /bounties`, `POST /reports`, etc.) importando `models` y `get_db`.
*   **Persona 2 (Frontend):** Puedes inicializar el proyecto de Vite/React en la carpeta `frontend/` y diseñar las pantallas basándote en los campos de `models.py`.
*   **Persona 3 (Blockchain):** Podemos empezar a diseñar cómo el backend ejecutará las transacciones hacia Stellar SDK y cómo guardaremos el `stellar_tx_hash`.   