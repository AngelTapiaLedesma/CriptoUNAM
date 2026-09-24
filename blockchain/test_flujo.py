# Archivo: backend/blockchain/test_flujo.py

from stellar_service import (
    crear_cuenta_escrow, 
    registrar_evidencia_en_blockchain, 
    pagar_recompensa_desde_escrow,
    registrar_proof_of_remediation
)
import hashlib
import time

# Usa las llaves que generamos en el paso 1 (las que tienen 10,000 XLM)
SECRET_EMPRESA = "SAFTQHDFS3GLSYQ2KMVLDLZRESNHOKK55I3HTPMYHKLFGRBZDAUPRX6V"
PUBLIC_INVESTIGADOR = "GCRW23YCSJGBHQEBTTFLQKW26LQ6GJBZ5PFWE64SCZQK7SGNWCQKUUTE"

monto_recompensa = "500"

print("\n--- 1. EMPRESA CREA BOUNTY (FONDOS COMPROMETIDOS / ESCROW) ---")
escrow = crear_cuenta_escrow(SECRET_EMPRESA, monto_recompensa)
print(f"Escrow creado y fondeado. TX: https://stellar.expert/explorer/testnet/tx/{escrow['tx_hash']}")

# Esperamos un poco para que Stellar procese la cuenta
time.sleep(3)

print("\n--- 2. INVESTIGADOR REPORTA (EVIDENCIA EN BLOCKCHAIN) ---")
reporte = "SQL Injection in /login"
hash_reporte = hashlib.sha256(reporte.encode()).hexdigest()
tx_evidencia = registrar_evidencia_en_blockchain(SECRET_EMPRESA, hash_reporte)
print(f"Evidencia registrada. TX: https://stellar.expert/explorer/testnet/tx/{tx_evidencia}")

print("\n--- 3. TRIAGER VALIDA Y PAGA ---")
tx_pago = pagar_recompensa_desde_escrow(escrow['escrow_secret'], PUBLIC_INVESTIGADOR, monto_recompensa)
print(f"Pago liberado al investigador. TX: https://stellar.expert/explorer/testnet/tx/{tx_pago}")

print("\n--- 4. EMPRESA CORRIGE EL ERROR (PROOF OF REMEDIATION) ---")
tx_remediation = registrar_proof_of_remediation(SECRET_EMPRESA, hash_reporte)
print(f"Certificado de corrección registrado. TX: https://stellar.expert/explorer/testnet/tx/{tx_remediation}")