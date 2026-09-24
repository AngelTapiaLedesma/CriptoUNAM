

---

# 🔗 PatchProof - Módulo Blockchain (Stellar Testnet)

Este submódulo maneja toda la lógica descentralizada de PatchProof usando la red de prueba de Stellar. Provee funciones listas para ser consumidas por el backend (FastAPI) sin necesidad de interactuar directamente con la blockchain o programar smart contracts.

## ⚙️ Requisitos previos (Para Persona 1 - Backend)

Asegúrate de instalar el SDK de Stellar en el entorno virtual donde esté corriendo FastAPI:

```bash
pip install stellar-sdk

```

## 🔐 Credenciales de Prueba (Testnet)

Para agilizar el desarrollo y la integración durante el hackathon, **las llaves de Stellar Testnet se dejaron directamente en el código**. Al ser fondos de prueba sin valor real, esto permite que cualquier miembro del equipo clone el repositorio y ejecute la demo inmediatamente sin necesidad de configurar variables de entorno locales.

*Las variables `SECRET_EMPRESA` y `PUBLIC_INVESTIGADOR` ya están definidas y fondeadas dentro de los scripts.*

## 🚀 Guía de Integración (`stellar_service.py`)

A continuación se detalla dónde y cómo invocar cada función dentro de los endpoints de FastAPI para cumplir el flujo del MVP.

### 1. Crear Escrow (Fondos Comprometidos)

* **Dónde usarlo:** En el endpoint `POST /bounties` (Cuando la EMPRESA crea un programa).
* **Qué hace:** Genera una wallet temporal (Escrow) y la fondea con el monto de la recompensa para garantizar la liquidez.

```python
from blockchain.stellar_service import crear_cuenta_escrow

# Retorna un diccionario con: escrow_public, escrow_secret y tx_hash
# Utiliza la variable SECRET_EMPRESA que ya está en el archivo
escrow_data = crear_cuenta_escrow(SECRET_EMPRESA, "500")

# ⚠️ IMPORTANTE: Debes guardar 'escrow_secret' en la base de datos 
# asociado a este Bounty, lo necesitaremos para hacer el pago después.

```

### 2. Registrar Evidencia (Submit Report)

* **Dónde usarlo:** En el endpoint `POST /reports` (Cuando el INVESTIGADOR envía una vulnerabilidad).
* **Qué hace:** Guarda el SHA-256 del reporte en la blockchain para generar evidencia criptográfica inmutable, manteniendo el contenido real off-chain.

```python
from blockchain.stellar_service import registrar_evidencia_en_blockchain

# Retorna el ID de la transacción en Stellar (str)
tx_evidencia = registrar_evidencia_en_blockchain(SECRET_EMPRESA, hash_del_reporte_generado)

# Guarda tx_evidencia en la BD asociado al Reporte para mostrarlo en el Frontend

```

### 3. Liberar Pago (Triager Validate)

* **Dónde usarlo:** En el endpoint `POST /reports/{id}/validate` (Cuando el TRIAGER aprueba el reporte).
* **Qué hace:** Transfiere los fondos desde la cuenta Escrow hacia la wallet del Investigador.

```python
from blockchain.stellar_service import pagar_recompensa_desde_escrow

# Recupera el escrow_secret de la BD y ejecuta el pago hacia PUBLIC_INVESTIGADOR
tx_pago = pagar_recompensa_desde_escrow(escrow_secret_bd, PUBLIC_INVESTIGADOR, "500")

```

### 4. Prueba de Remediación (Proof of Remediation)

* **Dónde usarlo:** En el endpoint `POST /reports/{id}/remediate` (Cuando la EMPRESA soluciona el fallo).
* **Qué hace:** Registra un nuevo hash en la red certificando que el reporte original fue parcheado, cerrando el ciclo.

```python
from blockchain.stellar_service import registrar_proof_of_remediation

tx_remediation = registrar_proof_of_remediation(SECRET_EMPRESA, hash_del_reporte_original)

```

## 🧪 Pruebas locales (Para Persona 4 - QA/Integración)

Para verificar que la conexión con Stellar Testnet funciona correctamente antes de levantar el servidor FastAPI, ejecuta el script de pruebas en la terminal:

```bash
python test_flujo.py

```

El script ejecutará el ciclo completo y devolverá URLs directas al explorador de bloques (Stellar Expert) para comprobar que los hashes y pagos se registran en vivo.
