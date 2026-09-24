import requests
from stellar_sdk import Keypair

def generar_wallet_nueva(nombre_actor):
    print(f"\n--- Creando Wallet para: {nombre_actor} ---")
    
    # 1. Generamos las llaves criptográficas (Esto ES la wallet)
    llaves = Keypair.random()
    public_key = llaves.public_key
    secret_key = llaves.secret
    
    print(f"Llave Pública (Cuenta): {public_key}")
    print(f"Llave Secreta (Password - NO COMPARTIR EN PROD): {secret_key}")
    
    # 2. Pedimos 10,000 XLM de prueba a Friendbot
    print("⏳ Pidiendo fondos de prueba a Friendbot...")
    respuesta = requests.get(f"https://friendbot.stellar.org/?addr={public_key}")
    
    if respuesta.status_code == 200:
        print("✅ ¡Éxito! La cuenta ahora tiene 10,000 TEST-XLM.")
        print(f"👀 Ver en el explorador: https://stellar.expert/explorer/testnet/account/{public_key}")
    else:
        print("❌ Error al pedir fondos.")
        
    return public_key, secret_key

# Vamos a crear las dos wallets que necesitamos para la demo
print("INICIANDO GENERACIÓN DE WALLETS PARA PATCHPROOF...")

pub_empresa, sec_empresa = generar_wallet_nueva("EMPRESA (La que paga el Bounty)")
pub_investigador, sec_investigador = generar_wallet_nueva("INVESTIGADOR (El que reporta y cobra)")

print("\n GUARDA ESTAS LLAVES EN UN BLOC DE NOTAS PARA USARLAS EN LA DEMO.")