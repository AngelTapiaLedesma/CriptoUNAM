const statusOrder = [
  'SUBMITTED',
  'VALIDATED',
  'PAID',
  'REMEDIATED',
  'VERIFIED',
]

const statusLabels = {
  SUBMITTED: 'Reporte enviado',
  VALIDATED: 'Reporte validado',
  PAID: 'Recompensa pagada',
  REMEDIATED: 'Vulnerabilidad remediada',
  VERIFIED: 'Corrección verificada',
}

function ReportTimeline({ report }) {
  const currentStatusIndex = statusOrder.indexOf(report.status)

  return (
    <div className="report-detail">

      <div className="detail-header">
        <div>
          <p className="section-label">Seguimiento</p>
          <h3>Ciclo de vida del reporte</h3>
        </div>

        <span
          className={`status-badge ${report.status.toLowerCase()}`}
        >
          {report.status}
        </span>
      </div>

      <div className="timeline">

        {statusOrder.map((status, index) => {
          const completed = index <= currentStatusIndex

          return (
            <div
              className={`timeline-step ${
                completed ? 'completed' : ''
              }`}
              key={status}
            >
              <div className="timeline-marker">
                {completed ? '✓' : ''}
              </div>

              <div>
                <strong>{statusLabels[status]}</strong>

                <span>
                  {completed
                    ? 'Etapa completada'
                    : 'Pendiente'}
                </span>
              </div>
            </div>
          )
        })}

      </div>

      <div className="blockchain-info">

        <div>
          <span className="info-label">
            Recompensa
          </span>

          <strong>
            {report.reward
              ? `${report.reward} XLM`
              : 'Pendiente'}
          </strong>
        </div>

        <div>
          <span className="info-label">
            Hash de evidencia
          </span>

          <strong className="hash-value">
            {report.evidenceHash}
          </strong>
        </div>

        <div>
          <span className="info-label">
            Transacción
          </span>

          <strong className="hash-value">
            {report.transactionHash || 'Sin transacción'}
          </strong>
        </div>

      </div>

    </div>
  )
}

export default ReportTimeline