from hashing import generate_salt, generate_report_hash

# Simulamos los datos que enviará el investigador
reporte_ficticio = "Vulnerabilidad de Authentication Bypass en el endpoint /api/v1/login."

# 1. Generamos un salt único para este reporte
salt = generate_salt()
print(f"Salt generado: {salt}")

# 2. Generamos el hash final
hash_resultado = generate_report_hash(reporte_ficticio, salt)
print(f"Hash SHA-256 para la blockchain: {hash_resultado}")