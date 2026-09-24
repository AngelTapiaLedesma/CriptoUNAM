import json

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, engine
import models
import hashing
import schemas
from states import transition_is_allowed

# Como medida de seguridad, aseguramos que las tablas existan al arrancar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PatchProof API", description="API para el MVP de PatchProof (GOYA HACK 2026)")

# Configuracion de CORS: Indispensable para que el frontend en React pueda hacer peticiones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitimos cualquier origen para agilizar el desarrollo del MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "online", 
        "message": "PatchProof API funcionando. Visita /docs para ver los endpoints."
    }

def report_to_response(
    report: models.Report,
    bounty: models.Bounty,
):
    return {
        "id": report.id,

        "bountyId": report.bounty_id,

        "title": report.title,

        "company": bounty.company,

        "severity": report.severity,

        "description": report.description,

        "status": report.status,

        "researcher": report.researcher,

        "submittedAt": report.created_at,

        "reward": bounty.reward,

        "evidenceHash": report.hash,

        "transactionHash": (
            report.stellar_tx_hash
        ),
    }

@app.post(
    "/reports",
    response_model=schemas.ReportResponse,
    status_code=201,
)
def create_report(
    data: schemas.ReportCreate,
    db: Session = Depends(get_db),
):

    bounty = (
        db.query(models.Bounty)
        .filter(
            models.Bounty.id
            == data.bounty_id
        )
        .first()
    )

    if bounty is None:
        raise HTTPException(
            status_code=404,
            detail="Bounty not found",
        )

    report_content = {
        "bounty_id": data.bounty_id,
        "researcher": data.researcher,
        "title": data.title,
        "description": data.description,
        "severity": data.severity,
        "evidence": data.evidence,
    }

    canonical_report = json.dumps(
        report_content,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    salt = hashing.generate_salt()

    report_hash = (
        hashing.generate_report_hash(
            canonical_report,
            salt,
        )
    )

    report = models.Report(
        bounty_id=data.bounty_id,
        researcher=data.researcher,
        title=data.title,
        description=data.description,
        severity=data.severity,
        evidence=data.evidence,
        salt=salt,
        hash=report_hash,
        status="SUBMITTED",
    )

    db.add(report)

    db.commit()

    db.refresh(report)

    return report_to_response(
        report,
        bounty,
    )

@app.get(
    "/reports",
    response_model=list[
        schemas.ReportResponse
    ],
)
def get_reports(
    db: Session = Depends(get_db),
):

    reports = (
        db.query(models.Report)
        .all()
    )

    response = []

    for report in reports:

        bounty = (
            db.query(models.Bounty)
            .filter(
                models.Bounty.id
                == report.bounty_id
            )
            .first()
        )

        if bounty is not None:
            response.append(
                report_to_response(
                    report,
                    bounty,
                )
            )

    return response

@app.get(
    "/reports/{report_id}",
    response_model=schemas.ReportResponse,
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
):

    report = (
        db.query(models.Report)
        .filter(
            models.Report.id
            == report_id
        )
        .first()
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    bounty = (
        db.query(models.Bounty)
        .filter(
            models.Bounty.id
            == report.bounty_id
        )
        .first()
    )

    return report_to_response(
        report,
        bounty,
    )

@app.patch(
    "/reports/{report_id}/status",
    response_model=schemas.ReportResponse,
)
def update_report_status(
    report_id: int,
    update: schemas.ReportStatusUpdate,
    db: Session = Depends(get_db),
):

    report = (
        db.query(models.Report)
        .filter(
            models.Report.id
            == report_id
        )
        .first()
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    current_status = (
        schemas.ReportStatus(
            report.status
        )
    )

    new_status = update.status

    if not transition_is_allowed(
        current_status,
        new_status,
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "Invalid status transition: "
                f"{current_status.value} "
                f"-> {new_status.value}"
            ),
        )

    report.status = new_status.value

    db.commit()

    db.refresh(report)

    bounty = (
        db.query(models.Bounty)
        .filter(
            models.Bounty.id
            == report.bounty_id
        )
        .first()
    )

    return report_to_response(
        report,
        bounty,
    )