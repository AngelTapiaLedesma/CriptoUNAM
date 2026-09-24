# Archivo: backend/blockchain/stellar_service.py

from stellar_sdk import Server, Keypair, TransactionBuilder, Network, HashMemo, Asset

# Conectamos a la Testnet
server = Server("https://horizon-testnet.stellar.org")
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE

def registrar_evidencia_en_blockchain(secret_empresa: str, hash_reporte: str) -> str:
    """
    Toma el SHA-256 del reporte y lo guarda en la blockchain en el campo Memo.
    """
    try:
        # Cargamos la cuenta de la empresa usando su llave secreta
        llaves_empresa = Keypair.from_secret(secret_empresa)
        cuenta_origen = server.load_account(llaves_empresa.public_key)
        
        # Armamos una transacción de 0.0000001 XLM de la empresa hacia sí misma 
        tx = (
            TransactionBuilder(
                source_account=cuenta_origen,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100
            )
            .append_payment_op(
                destination=llaves_empresa.public_key, 
                amount="0.0000001", 
                asset=Asset.native()
            )
            .add_memo(HashMemo(hash_reporte)) # Guardamos el Hash
            .set_timeout(30)
            .build()
        )
        
        # Firmamos y enviamos
        tx.sign(llaves_empresa)
        respuesta = server.submit_transaction(tx)
        
        return respuesta["hash"] # Retorna el ID de la transacción
        
    except Exception as e:
        print(f"Error al registrar evidencia: {e}")
        return None

def pagar_recompensa(secret_empresa: str, public_investigador: str, cantidad_xlm: str) -> str:
    """
    Envía los fondos de la empresa al investigador cuando el Triager aprueba el reporte.
    """
    try:
        llaves_empresa = Keypair.from_secret(secret_empresa)
        cuenta_origen = server.load_account(llaves_empresa.public_key)
        
        tx = (
            TransactionBuilder(
                source_account=cuenta_origen,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100
            )
            .append_payment_op(
                destination=public_investigador,
                amount=str(cantidad_xlm),
                asset=Asset.native()
            )
            .set_timeout(30)
            .build()
        )
        
        tx.sign(llaves_empresa)
        respuesta = server.submit_transaction(tx)
        
        return respuesta["hash"]
        
    except Exception as e:
        print(f"Error en el pago: {e}")
        return None