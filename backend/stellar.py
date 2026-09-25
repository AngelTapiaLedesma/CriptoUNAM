def release_reward(
    destination: str,
    amount: str,
) -> str:

    raise NotImplementedError(
        "Stellar integration "
        "not connected yet"
    )

# Archivo: backend/stellar.py

from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset, HashMemo
import hashlib

server = Server("https://horizon-testnet.stellar.org")
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE

# Llaves fijas de Testnet para el MVP
SECRET_EMPRESA = "SAFTQHDFS3GLSYQ2KMVLDLZRESNHOKK55I3HTPMYHKLFGRBZDAUPRX6V"
PUBLIC_INVESTIGADOR = "GCRW23YCSJGBHQEBTTFLQKW26LQ6GJBZ5PFWE64SCZQK7SGNWCQKUUTE"

def crear_cuenta_escrow(secret_empresa: str, monto_bounty: str) -> dict:
    try:
        llaves_empresa = Keypair.from_secret(secret_empresa)
        cuenta_empresa = server.load_account(llaves_empresa.public_key)
        escrow_keypair = Keypair.random()
        
        tx = (
            TransactionBuilder(
                source_account=cuenta_empresa,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100
            )
            .append_create_account_op(
                destination=escrow_keypair.public_key,
                starting_balance=str(float(monto_bounty) + 2.0)
            )
            .set_timeout(30)
            .build()
        )
        tx.sign(llaves_empresa)
        respuesta = server.submit_transaction(tx)
        return {
            "escrow_public": escrow_keypair.public_key,
            "escrow_secret": escrow_keypair.secret,
            "tx_hash": respuesta["hash"]
        }
    except Exception as e:
        print(f"Error Escrow: {e}")
        return None

def registrar_evidencia_en_blockchain(secret_empresa: str, hash_reporte: str) -> str:
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
                destination=llaves_empresa.public_key, 
                amount="0.0000001", 
                asset=Asset.native()
            )
            .add_memo(HashMemo(hash_reporte))
            .set_timeout(300)
            .build()
        )
        tx.sign(llaves_empresa)
        return server.submit_transaction(tx)["hash"]
    except Exception as e:
        print(f"Error Evidencia: {e}")
        return None

def pagar_recompensa_desde_escrow(secret_origen: str, public_destino: str, monto: str) -> str:
    try:
        llaves_origen = Keypair.from_secret(secret_origen)
        cuenta_origen = server.load_account(llaves_origen.public_key)
        
        tx = (
            TransactionBuilder(
                source_account=cuenta_origen,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100
            )
            .append_payment_op(
                destination=public_destino,
                amount=str(monto),
                asset=Asset.native()
            )
            .set_timeout(30)
            .build()
        )
        tx.sign(llaves_origen)
        return server.submit_transaction(tx)["hash"]
    except Exception as e:
        print(f"Error Pago: {e}")
        return None

def registrar_proof_of_remediation(secret_empresa: str, hash_reporte_original: str) -> str:
    try:
        remediation_data = f"REMEDIATED:{hash_reporte_original}"
        remediation_hash = hashlib.sha256(remediation_data.encode()).hexdigest()

        llaves_empresa = Keypair.from_secret(secret_empresa)
        cuenta_origen = server.load_account(llaves_empresa.public_key)
        
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
            .add_memo(HashMemo(remediation_hash))
            .set_timeout(30)
            .build()
        )
        tx.sign(llaves_empresa)
        return server.submit_transaction(tx)["hash"]
    except Exception as e:
        print(f"Error Proof of Remediation: {e}")
        return None