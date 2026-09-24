import requests
from stellar_sdk import Keypair

def generar_y_fondear(nombre):
    llaves = Keypair.random()
    print(f"Fondeando {nombre}...")
    # Pedimos fondos de prueba al bot de Stellar
    requests.get(f"https://friendbot.stellar.org/?addr={llaves.public_key}")
    print(f"Llave Pública (G...): {llaves.public_key}")
    print(f"Llave Secreta (S...): {llaves.secret}\n")

print("--- EMPRESA ---")
generar_y_fondear("EMPRESA")

print("--- INVESTIGADOR ---")
generar_y_fondear("INVESTIGADOR")