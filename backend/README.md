# Resumen de Integración y Desarrollo Backend
**Autor:** Lael (Backend / Flujo del Reporte)  
**Objetivo:** Integrar la infraestructura base de Backend y Base de Datos desarrollada previamente con la lógica correspondiente al flujo de reportes de PatchProof, incluyendo endpoints FastAPI, generación de hash SHA-256, persistencia en SQLite, control de estados y preparación para la integración posterior con Stellar Testnet.

## 1. Integración con la Base de Datos
Se integró el trabajo previamente desarrollado para la capa de Base de Datos utilizando SQLite y SQLAlchemy.

*   **`backend/database.py`:** Configura la conexión con SQLite y proporciona la dependencia `get_db()` para utilizar sesiones de base de datos dentro de los endpoints.
*   **`backend/models.py`:** Contiene los modelos `Bounty` y `Report`.
*   **`backend/init_db.py`:** Permite generar localmente la base de datos `patchproof_mvp.db`.
*   **`backend/seed_db.py`:** Inserta Bounties ficticios para probar el flujo del MVP sin depender todavía del frontend.
*   **`backend/requirements.txt`:** Contiene las dependencias requeridas para ejecutar FastAPI, SQLAlchemy, Pydantic y Uvicorn.
*   **Cambio agregado:** Se añadió el campo `salt` al modelo `Report` para conservar el valor utilizado durante la generación del SHA-256 y permitir posteriormente verificar la integridad del reporte.

## 2. Flujo de Reportes con FastAPI
Se implementó en **`backend/main.py`** la lógica principal correspondiente al ciclo de vida de los reportes.

Los endpoints actualmente disponibles son:

*   **`POST /reports`:** Recibe un nuevo reporte de vulnerabilidad, genera su evidencia criptográfica y lo registra con estado `SUBMITTED`.
*   **`GET /reports`:** Obtiene la lista de reportes registrados.
*   **`GET /reports/{report_id}`:** Obtiene un reporte específico mediante su identificador.
*   **`PATCH /reports/{report_id}/status`:** Actualiza el estado del reporte validando que la transición sea permitida.

El flujo de creación del reporte es:

```text
Reporte recibido
        ↓
Validación con Pydantic
        ↓
Consulta del Bounty
        ↓
Normalización del contenido
        ↓
Generación de Salt
        ↓
Generación SHA-256
        ↓
Persistencia en SQLite
        ↓
Status = SUBMITTED
```

La respuesta del backend incluye información como:

```json
{
  "id": 1,
  "status": "SUBMITTED",
  "evidenceHash": "...",
  "transactionHash": null
}
```

La evidencia completa permanece almacenada fuera de blockchain.

## 3. Esquemas de Entrada y Salida
Se agregó el archivo:

*   **`backend/schemas.py`:** Define los modelos Pydantic utilizados por la API.

Entre los esquemas principales se encuentran:

*   **`ReportCreate`:** Define los datos requeridos para crear un reporte.
*   **`ReportResponse`:** Define la estructura que devuelve el backend al frontend.
*   **`ReportStatusUpdate`:** Define la actualización del estado.
*   **`ReportStatus`:** Enumera los estados permitidos.

También funciona como capa de adaptación entre los nombres utilizados internamente en SQLite y los nombres utilizados por el frontend.

```text
Base de Datos          Frontend
bounty_id       →      bountyId
created_at      →      submittedAt
hash            →      evidenceHash
stellar_tx_hash →      transactionHash
```

Esto permite integrar el backend con React sin modificar la estructura principal de la Base de Datos.

## 4. Lógica Criptográfica (Off-Chain a On-Chain)
Se utiliza el archivo:

*   **`backend/hashing.py`:** Contiene las funciones para generar un `salt` aleatorio y calcular el hash SHA-256 del reporte.

El proceso utilizado es:

```text
Contenido del reporte
        +
Salt aleatorio
        ↓
SHA-256
        ↓
Hash de 64 caracteres hexadecimales
```

Conceptualmente:

```text
SHA256(report_content + salt)
```

El hash representa la evidencia verificable del reporte que posteriormente podrá relacionarse con Stellar Testnet sin publicar información sensible sobre la vulnerabilidad.

## 5. Control del Ciclo de Vida del Reporte
Se agregó:

*   **`backend/states.py`:** Controla las transiciones permitidas entre estados.

El flujo principal implementado es:

```text
SUBMITTED
    ↓
VALIDATED
    ↓
PAID
    ↓
REMEDIATED
    ↓
VERIFIED
```

También se contemplan los estados:

*   **`NEEDS_INFORMATION`**
*   **`REJECTED`**

El backend impide transiciones inválidas.

Por ejemplo:

```text
SUBMITTED → PAID
```

no está permitido porque primero debe existir:

```text
SUBMITTED → VALIDATED → PAID
```

Cuando se intenta una transición inválida, la API devuelve:

```text
409 Conflict
```

## 6. Integración con el Frontend
La API mantiene compatibilidad con el servicio preparado por la **Persona 2 (Frontend)** en React/Vite.

El frontend puede utilizar:

*   **`GET /reports`**
*   **`POST /reports`**
*   **`PATCH /reports/{id}/status`**

La respuesta del backend contiene los campos principales requeridos por la interfaz:

```text
id
bountyId
title
company
severity
description
status
researcher
submittedAt
reward
evidenceHash
transactionHash
```

*   **CORS Habilitado:** Se mantiene la configuración necesaria para permitir peticiones locales desde React hacia `http://localhost:8000`.

## 7. Preparación para Stellar
Se agregó:

*   **`backend/stellar.py`:** Punto de integración para conectar posteriormente el backend con Stellar Testnet.

Actualmente contiene la interfaz inicial:

```text
release_reward(destination, amount)
```

El objetivo es que posteriormente la **Persona 3 (Blockchain)** pueda conectar Stellar Testnet sin modificar la lógica principal del flujo de reportes.

El flujo esperado será:

```text
VALIDATED
    ↓
Backend Python
    ↓
Stellar Testnet
    ↓
Pago confirmado
    ↓
transactionHash
    ↓
PAID
```

Actualmente el cambio a `PAID` funciona como parte de la lógica de estados. La ejecución del pago real mediante Stellar queda como siguiente etapa de integración.

## 8. Ejecución del Backend
Desde la carpeta `backend/`:

*   **Activar el entorno virtual:**

```powershell
.\.venv\Scripts\Activate.ps1
```

*   **Instalar dependencias:**

```powershell
pip install -r requirements.txt
```

*   **Generar la Base de Datos:**

```powershell
python init_db.py
```

*   **Insertar datos ficticios:**

```powershell
python seed_db.py
```

*   **Levantar FastAPI:**

```powershell
uvicorn main:app --reload
```

*   **Documentación interactiva:** `http://127.0.0.1:8000/docs`

## 9. Estado Actual
Actualmente se encuentra funcional:

*   **FastAPI**
*   **SQLite + SQLAlchemy**
*   **Creación y persistencia de reportes**
*   **Generación de salt**
*   **Generación SHA-256**
*   **Consulta general e individual de reportes**
*   **Actualización de estados**
*   **Validación de transiciones**
*   **Flujo `SUBMITTED → VALIDATED → PAID → REMEDIATED → VERIFIED`**
*   **Compatibilidad con el contrato actual del frontend**
*   **Preparación de la interfaz para Stellar**

## 10. Siguientes Pasos Inmediatos
*   **Persona 1 (Backend):** Conectar el flujo `VALIDATED → PAID` con la integración real de Stellar y guardar el `stellar_tx_hash`.
*   **Persona 2 (Frontend):** Consumir los endpoints del backend para mostrar reportes, hashes, estados y transacciones.
*   **Persona 3 (Blockchain):** Integrar Stellar Testnet y devolver el `transactionHash` real al backend.
*   **Persona 4 (Integración / Base de Datos):** Continuar apoyando la integración general, pruebas y consistencia de la Base de Datos.
*   **Equipo:** Probar el flujo completo de la demo desde el envío del reporte hasta la remediación y verificación.