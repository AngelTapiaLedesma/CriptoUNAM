# Archivo: backend/blockchain/test_flujo.py

from stellar_service import registrar_evidencia_en_blockchain, pagar_recompensa
import hashlib

# 1. Pega aquí las llaves que te dio tu script anterior (1_crear_wallets.py)
SECRET_EMPRESA = "SCXWDP34FAMJPEX4HNJ4HF2NUY3LSVLHNMFF5ADYF6YD7WDFMGE3LAGD"
PUBLIC_INVESTIGADOR = "GD72X6PTJY7OI6CZLFWPRYPGPZUNXHQVRN2VYWNPYZOSQN4Q4TN2GVXT"

print("\n--- SIMULANDO FLUJO DE PATCHPROOF ---")

# 2. Simulamos que la Persona 1 (Backend) recibe un reporte y genera el SHA-256
reporte_falso = "Vulnerabilidad XSS en el login de la empresa."
# Creamos el hash (debe ser de 64 caracteres exactos en hexadecimal)
hash_del_reporte = hashlib.sha256(reporte_falso.encode()).hexdigest()
print(f"1️⃣ Hash generado: {hash_del_reporte}")

# 3. Guardamos el hash en Stellar
print("2️⃣ Registrando evidencia en la blockchain...")
tx_evidencia = registrar_evidencia_en_blockchain(SECRET_EMPRESA, hash_del_reporte)
print(f"✅ Evidencia registrada! Ver transacción: https://stellar.expert/explorer/testnet/tx/{tx_evidencia}")

# 4. Simulamos que el Triager valida y paga
print("3️⃣ Triager validó el reporte. Pagando 500 TEST-XLM...")
tx_pago = pagar_recompensa(SECRET_EMPRESA, PUBLIC_INVESTIGADOR, "500")
print(f"✅ Pago realizado! Ver transacción: https://stellar.expert/explorer/testnet/tx/{tx_pago}")