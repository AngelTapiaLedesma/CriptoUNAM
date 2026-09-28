# Archivo: scripts/test_flujo.py

import hashlib
import os
import time
from pathlib import Path

from dotenv import load_dotenv

from stellar_service import (
    crear_cuenta_escrow,
    registrar_evidencia_en_blockchain,
    pagar_recompensa_desde_escrow,
    registrar_proof_of_remediation,
)


# Carga las credenciales desde backend/.env
ENV_PATH = (
    Path(__file__).resolve().parents[1]
    / "backend"
    / ".env"
)

load_dotenv(ENV_PATH)

SECRET_EMPRESA = os.getenv("STELLAR_SECRET_EMPRESA")
PUBLIC_INVESTIGADOR = os.getenv(
    "STELLAR_PUBLIC_INVESTIGADOR"
)

if not SECRET_EMPRESA:
    raise RuntimeError(
        "Falta STELLAR_SECRET_EMPRESA en backend/.env"
    )

if not PUBLIC_INVESTIGADOR:
    raise RuntimeError(
        "Falta STELLAR_PUBLIC_INVESTIGADOR en backend/.env"
    )


monto_recompensa = "500"


print(
    "\n--- 1. EMPRESA CREA BOUNTY "
    "(FONDOS COMPROMETIDOS / ESCROW) ---"
)

escrow = crear_cuenta_escrow(
    SECRET_EMPRESA,
    monto_recompensa,
)

if not escrow:
    raise RuntimeError(
        "No fue posible crear la cuenta escrow."
    )

print(
    "Escrow creado y fondeado. TX: "
    "https://stellar.expert/explorer/testnet/tx/"
    f"{escrow['tx_hash']}"
)


time.sleep(3)


print(
    "\n--- 2. INVESTIGADOR REPORTA "
    "(EVIDENCIA EN BLOCKCHAIN) ---"
)

reporte = "SQL Injection in /login"

hash_reporte = hashlib.sha256(
    reporte.encode()
).hexdigest()

tx_evidencia = registrar_evidencia_en_blockchain(
    SECRET_EMPRESA,
    hash_reporte,
)

print(
    "Evidencia registrada. TX: "
    "https://stellar.expert/explorer/testnet/tx/"
    f"{tx_evidencia}"
)


print(
    "\n--- 3. TRIAGER VALIDA Y PAGA ---"
)

tx_pago = pagar_recompensa_desde_escrow(
    escrow["escrow_secret"],
    PUBLIC_INVESTIGADOR,
    monto_recompensa,
)

print(
    "Pago liberado al investigador. TX: "
    "https://stellar.expert/explorer/testnet/tx/"
    f"{tx_pago}"
)


print(
    "\n--- 4. EMPRESA CORRIGE EL ERROR "
    "(PROOF OF REMEDIATION) ---"
)

tx_remediation = registrar_proof_of_remediation(
    SECRET_EMPRESA,
    hash_reporte,
)

print(
    "Certificado de corrección registrado. TX: "
    "https://stellar.expert/explorer/testnet/tx/"
    f"{tx_remediation}"
)