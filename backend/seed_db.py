import json
from database import SessionLocal
import models

def seed_data():
    db = SessionLocal()
    try:
        # Verificamos si ya existen datos para evitar duplicados al correrlo varias veces
        if db.query(models.Bounty).count() > 0:
            print("La base de datos ya contiene Bounties. No se insertaron datos nuevos.")
            return

        bounty1 = models.Bounty(
            company="Fintech Corp",
            title="Bounty Principal - Plataforma Web",
            description="Buscamos vulnerabilidades en nuestra plataforma de pagos (auth bypass, SQLi, XSS). Quedan estrictamente prohibidas las pruebas de denegación de servicio (DDoS).",
            scope="*.fintech-demo.com",
            reward="500 TEST-XLM",
            severity_rewards=json.dumps({"CRITICAL": "500 TEST-XLM", "HIGH": "250 TEST-XLM"}),
            status="ACTIVE",
            stellar_address="GBDVL...FICTICIO...3A2X" # Simulación de la wallet Escrow
        )

        bounty2 = models.Bounty(
            company="Startup SaaS",
            title="Auditoría de API Gateway",
            description="Programa público para nuestra API v2. Solo se pagan reportes con impacto demostrable en la lógica de negocio.",
            scope="api.startup-saas.net",
            reward="1000 TEST-XLM",
            severity_rewards=json.dumps({"CRITICAL": "1000 TEST-XLM", "HIGH": "500 TEST-XLM", "MEDIUM": "100 TEST-XLM"}),
            status="ACTIVE",
            stellar_address="GCXYZ...FICTICIO...9B4Y"
        )

        db.add_all([bounty1, bounty2])
        db.commit()
        print("Bounties de prueba inyectados exitosamente en SQLite.")
        
    except Exception as e:
        print(f"Error al inyectar datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()