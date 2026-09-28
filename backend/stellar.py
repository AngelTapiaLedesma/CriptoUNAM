import hashlib
import os
from pathlib import Path

from dotenv import load_dotenv
from stellar_sdk import (
    Asset,
    HashMemo,
    Keypair,
    Network,
    Server,
    TransactionBuilder,
)


# Carga las variables definidas en backend/.env
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)


server = Server("https://horizon-testnet.stellar.org")
NETWORK_PASSPHRASE = Network.TESTNET_NETWORK_PASSPHRASE


SECRET_EMPRESA = os.getenv("STELLAR_SECRET_EMPRESA")
PUBLIC_INVESTIGADOR = os.getenv("STELLAR_PUBLIC_INVESTIGADOR")


if not SECRET_EMPRESA:
    raise RuntimeError(
        "Falta STELLAR_SECRET_EMPRESA en backend/.env"
    )

if not PUBLIC_INVESTIGADOR:
    raise RuntimeError(
        "Falta STELLAR_PUBLIC_INVESTIGADOR en backend/.env"
    )


def crear_cuenta_escrow(
    secret_empresa: str,
    monto_bounty: str,
) -> dict | None:
    try:
        llaves_empresa = Keypair.from_secret(
            secret_empresa
        )

        cuenta_empresa = server.load_account(
            llaves_empresa.public_key
        )

        escrow_keypair = Keypair.random()

        tx = (
            TransactionBuilder(
                source_account=cuenta_empresa,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_create_account_op(
                destination=escrow_keypair.public_key,
                starting_balance=str(
                    float(monto_bounty) + 2.0
                ),
            )
            .set_timeout(30)
            .build()
        )

        tx.sign(llaves_empresa)
        respuesta = server.submit_transaction(tx)

        return {
            "escrow_public": escrow_keypair.public_key,
            "escrow_secret": escrow_keypair.secret,
            "tx_hash": respuesta["hash"],
        }

    except Exception as error:
        print(f"Error Escrow: {error}")
        return None


def registrar_evidencia_en_blockchain(
    secret_empresa: str,
    hash_reporte: str,
) -> str | None:
    try:
        llaves_empresa = Keypair.from_secret(
            secret_empresa
        )

        cuenta_origen = server.load_account(
            llaves_empresa.public_key
        )

        tx = (
            TransactionBuilder(
                source_account=cuenta_origen,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_payment_op(
                destination=llaves_empresa.public_key,
                amount="0.0000001",
                asset=Asset.native(),
            )
            .add_memo(
                HashMemo(hash_reporte)
            )
            .set_timeout(300)
            .build()
        )

        tx.sign(llaves_empresa)

        return server.submit_transaction(tx)["hash"]

    except Exception as error:
        print(f"Error Evidencia: {error}")
        return None


def pagar_recompensa_desde_escrow(
    secret_origen: str,
    public_destino: str,
    monto: str,
) -> str | None:
    try:
        llaves_origen = Keypair.from_secret(
            secret_origen
        )

        cuenta_origen = server.load_account(
            llaves_origen.public_key
        )

        tx = (
            TransactionBuilder(
                source_account=cuenta_origen,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_payment_op(
                destination=public_destino,
                amount=str(monto),
                asset=Asset.native(),
            )
            .set_timeout(30)
            .build()
        )

        tx.sign(llaves_origen)

        return server.submit_transaction(tx)["hash"]

    except Exception as error:
        print(f"Error Pago: {error}")
        return None


def registrar_proof_of_remediation(
    secret_empresa: str,
    hash_reporte_original: str,
) -> str | None:
    try:
        remediation_data = (
            f"REMEDIATED:{hash_reporte_original}"
        )

        remediation_hash = hashlib.sha256(
            remediation_data.encode()
        ).hexdigest()

        llaves_empresa = Keypair.from_secret(
            secret_empresa
        )

        cuenta_origen = server.load_account(
            llaves_empresa.public_key
        )

        tx = (
            TransactionBuilder(
                source_account=cuenta_origen,
                network_passphrase=NETWORK_PASSPHRASE,
                base_fee=100,
            )
            .append_payment_op(
                destination=llaves_empresa.public_key,
                amount="0.0000001",
                asset=Asset.native(),
            )
            .add_memo(
                HashMemo(remediation_hash)
            )
            .set_timeout(30)
            .build()
        )

        tx.sign(llaves_empresa)

        return server.submit_transaction(tx)["hash"]

    except Exception as error:
        print(
            f"Error Proof of Remediation: {error}"
        )
        return None