import hashlib
import secrets

def generate_salt(length: int = 16) -> str:
    """Genera un salt aleatorio en formato hexadecimal."""
    return secrets.token_hex(length)

def generate_report_hash(report_content: str, salt: str) -> str:
    """
    Genera un hash SHA-256 combinando el contenido del reporte y el salt.
    Esta es la huella digital que se registrará en Stellar Testnet.
    """
    # Concatenamos el contenido y el salt siguiendo la especificación del MVP
    data_to_hash = f"{report_content}{salt}"
    
    # Generamos el hash SHA-256
    hash_object = hashlib.sha256(data_to_hash.encode('utf-8'))
    return hash_object.hexdigest()