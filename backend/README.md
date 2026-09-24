# Resumen de Integración y Desarrollo Backend

Autor: Lael (Backend / Flujo del Reporte)

Objetivo: Integrar la infraestructura base de Backend y Base de Datos desarrollada previamente con la lógica correspondiente al flujo de reportes de PatchProof, incluyendo endpoints FastAPI, generación de hash SHA-256, persistencia en SQLite, control de estados y preparación para la integración posterior con Stellar Testnet.

1. Integración con la Base de Datos

Se integró el trabajo previamente desarrollado para la capa de Base de Datos utilizando SQLite y SQLAlchemy.

La estructura utilizada incluye:

- backend/database.py: Configura la conexión con SQLite y proporciona la dependencia get_db() para utilizar sesiones de base de datos dentro de los endpoints.
- backend/models.py: Contiene los modelos Bounty y Report.
- backend/init_db.py: Permite generar localmente la base de datos patchproof_mvp.db.
- backend/seed_db.py: Inserta Bounties ficticios que permiten probar el flujo del MVP sin depender todavía del frontend.
- backend/requirements.txt: Contiene las dependencias requeridas para ejecutar FastAPI, SQLAlchemy, Pydantic y Uvicorn.

Además, se agregó al modelo Report el campo:

salt

para conservar el valor utilizado durante la generación del SHA-256 y permitir posteriormente verificar la integridad del reporte.

2. Flujo de Reportes con FastAPI

Se implementó en backend/main.py la lógica principal correspondiente al ciclo de vida de los reportes.

Los endpoints actualmente disponibles son:

POST   /reports
GET    /reports
GET    /reports/{report_id}
PATCH  /reports/{report_id}/status

POST /reports

Permite recibir un nuevo reporte de vulnerabilidad.

El flujo realizado por el backend es:

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

El backend devuelve información como:

{
  "id": 1,
  "status": "SUBMITTED",
  "evidenceHash": "...",
  "transactionHash": null
}

La evidencia completa permanece almacenada fuera de blockchain.

3. Esquemas de Entrada y Salida

Se agregó:

backend/schemas.py

Este archivo define los modelos Pydantic utilizados por la API.

Entre ellos se encuentran:

- ReportCreate
- ReportResponse
- ReportStatusUpdate
- ReportStatus

También funciona como capa de adaptación entre los nombres utilizados internamente en SQLite y los nombres que necesita el frontend.

Por ejemplo:

Base de Datos          Frontend

bounty_id       →      bountyId
created_at      →      submittedAt
hash            →      evidenceHash
stellar_tx_hash →      transactionHash

Esto permite integrar el backend con React sin modificar la estructura principal de la base de datos.

4. Generación de Evidencia Criptográfica

Se utiliza:

backend/hashing.py

para generar el hash criptográfico del reporte.

El proceso es:

Contenido del reporte
        +
Salt aleatorio
        ↓
SHA-256
        ↓
Hash de 64 caracteres hexadecimales

Conceptualmente:

SHA256(report_content + salt)

El hash representa la evidencia verificable del reporte que posteriormente podrá relacionarse con Stellar Testnet sin publicar información sensible sobre la vulnerabilidad.

5. Control del Ciclo de Vida del Reporte

Se agregó:

backend/states.py

para controlar las transiciones permitidas entre estados.

El flujo principal implementado es:

SUBMITTED
    ↓
VALIDATED
    ↓
PAID
    ↓
REMEDIATED
    ↓
VERIFIED

También se contemplan los estados:

NEEDS_INFORMATION
REJECTED

El backend impide transiciones inválidas.

Por ejemplo:

SUBMITTED → PAID

no está permitido porque primero debe existir:

SUBMITTED → VALIDATED → PAID

Cuando se intenta una transición inválida, la API devuelve:

409 Conflict

6. Integración con el Frontend

La API mantiene compatibilidad con el servicio preparado por la Persona 2 en React/Vite.

El frontend puede utilizar:

GET /reports
POST /reports
PATCH /reports/{id}/status

La respuesta del backend contiene los campos principales requeridos por la interfaz:

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

CORS continúa habilitado para permitir peticiones locales desde el frontend hacia:

http://localhost:8000

7. Preparación para Stellar

Se agregó:

backend/stellar.py

como punto de integración para la capa Blockchain.

Actualmente contiene la interfaz inicial:

release_reward(destination, amount)

El objetivo es que posteriormente la Persona 3 pueda conectar Stellar Testnet sin modificar la lógica principal del flujo de reportes.

El flujo esperado será:

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

Actualmente el cambio a PAID funciona como parte de la lógica de estados; la ejecución del pago real en Stellar queda como siguiente etapa de integración.

8. Ejecución del Backend

Desde la carpeta:

backend/

activar el entorno virtual:

.\.venv\Scripts\Activate.ps1

Instalar dependencias:

pip install -r requirements.txt

Generar la base de datos:

python init_db.py

Insertar datos ficticios:

python seed_db.py

Levantar FastAPI:

uvicorn main:app --reload

La documentación interactiva puede consultarse en:

http://127.0.0.1:8000/docs

9. Estado Actual

Actualmente se encuentra funcional:

✓ FastAPI
✓ SQLite + SQLAlchemy
✓ Creación de reportes
✓ Persistencia en Base de Datos
✓ Generación de salt
✓ Generación SHA-256
✓ GET de reportes
✓ Consulta individual de reportes
✓ Actualización de estados
✓ Validación de transiciones
✓ SUBMITTED → VALIDATED → PAID → REMEDIATED → VERIFIED
✓ Compatibilidad con el contrato actual del frontend
✓ Preparación de la interfaz para Stellar

10. Siguientes Pasos

- Conectar backend/stellar.py con la implementación de Stellar Testnet desarrollada por la Persona 3.
- Ejecutar el pago real únicamente cuando el reporte pase de VALIDATED a PAID.
- Guardar el hash real de la transacción Stellar en stellar_tx_hash.
- Integrar completamente frontend, backend, SQLite y Stellar.
- Realizar pruebas del flujo completo para la demo final.