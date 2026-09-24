# Archivo: backend/blockchain/stellar_service.py

from stellar_sdk import Server, Keypair, TransactionBuilder, Network, HashMemo, Asset
import hashlib

server = Server("https://horizon-testnet.stellar.org")
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE

def crear_cuenta_escrow(secret_empresa: str, monto_bounty: str) -> dict:
    """
    CUMPLE PUNTO A) ESCROW.
    Crea una cuenta temporal que retendrá los fondos del bounty.
    Garantiza que la empresa no pueda gastar ese dinero en otra cosa.
    """
    try:
        llaves_empresa = Keypair.from_secret(secret_empresa)
        cuenta_empresa = server.load_account(llaves_empresa.public_key)
        
        # Generamos la wallet que servirá de Escrow
        escrow_keypair = Keypair.random()
        
        # La empresa crea y fondea el Escrow con el monto de la recompensa
        tx = (
            TransactionBuilder(
                source_account=cuenta_empresa,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100
            )
            .append_create_account_op(
                destination=escrow_keypair.public_key,
                starting_balance=str(float(monto_bounty) + 2.0) # Monto + reserva mínima de Stellar
            )
            .set_timeout(30)
            .build()
        )
        
        tx.sign(llaves_empresa)
        respuesta = server.submit_transaction(tx)
        
        print(f"✅ Escrow fondeado. TX: {respuesta['hash']}")
        return {
            "escrow_public": escrow_keypair.public_key,
            "escrow_secret": escrow_keypair.secret,
            "tx_hash": respuesta["hash"]
        }
    except Exception as e:
        print(f"❌ Error al crear Escrow: {e}")
        return None

def registrar_evidencia_en_blockchain(secret_empresa: str, hash_reporte: str) -> str:
    """
    CUMPLE PUNTO B) EVIDENCIA DEL REPORTE.
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
                destination=llaves_empresa.public_key, 
                amount="0.0000001", 
                asset=Asset.native()
            )
            .add_memo(HashMemo(hash_reporte))
            .set_timeout(30)
            .build()
        )
        tx.sign(llaves_empresa)
        return server.submit_transaction(tx)["hash"]
    except Exception as e:
        print(f"❌ Error en evidencia: {e}")
        return None

def pagar_recompensa_desde_escrow(secret_escrow: str, public_investigador: str, monto: str) -> str:
    """
    CUMPLE PUNTO D) PAGO.
    Transfiere los fondos desde la cuenta Escrow al Investigador.
    """
    try:
        llaves_escrow = Keypair.from_secret(secret_escrow)
        cuenta_escrow = server.load_account(llaves_escrow.public_key)
        
        tx = (
            TransactionBuilder(
                source_account=cuenta_escrow,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100
            )
            .append_payment_op(
                destination=public_investigador,
                amount=str(monto),
                asset=Asset.native()
            )
            .set_timeout(30)
            .build()
        )
        tx.sign(llaves_escrow)
        return server.submit_transaction(tx)["hash"]
    except Exception as e:
        print(f"❌ Error en pago: {e}")
        return None

def registrar_proof_of_remediation(secret_empresa: str, hash_reporte_original: str) -> str:
    """
    CUMPLE PUNTO E) PROOF OF REMEDIATION.
    Registra que la vulnerabilidad fue parcheada. Usamos el hash original + la palabra 'REMEDIATED'
    para generar un nuevo hash que certifique la corrección.
    """
    try:
        # Generamos un nuevo hash que une el reporte original con la acción de parcheo
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
        print(f"❌ Error en Proof of Remediation: {e}")
        return None