function Company({ reports, setReports }) {
  const company = 'NovaPay'

  const companyReports = reports.filter(
    (report) => report.company === company
  )

  const rewardBySeverity = {
    Critical: 850,
    High: 500,
    Medium: 250,
    Low: 100,
  }

  const payReward = (reportId) => {
    const updatedReports = reports.map((report) =>
      report.id === reportId
        ? {
            ...report,
            status: 'PAID',
            reward: rewardBySeverity[report.severity],
            transactionHash: `tx-${Date.now().toString(16)}`,
          }
        : report
    )

    setReports(updatedReports)
  }

  const markRemediated = (reportId) => {
    const updatedReports = reports.map((report) =>
      report.id === reportId
        ? {
            ...report,
            status: 'REMEDIATED',
          }
        : report
    )

    setReports(updatedReports)
  }

  return (
    <div className="company-page">

      <div className="page-heading">
        <div>
          <p className="section-label">Empresa</p>
          <h2>Vulnerabilidades de {company}</h2>

          <p className="section-description">
            Gestiona las vulnerabilidades validadas, recompensas y
            avances de remediación.
          </p>
        </div>

        <div className="company-badge">
          {company}
        </div>
      </div>

      <div className="company-reports">

        {companyReports.map((report) => (
          <div className="company-report-card" key={report.id}>

            <div className="company-report-header">

              <div>
                <div className="report-card-top">

                  <span className="report-id">
                    {report.id}
                  </span>

                  <span
                    className={`severity-badge ${report.severity.toLowerCase()}`}
                  >
                    {report.severity}
                  </span>

                </div>

                <h3>{report.title}</h3>

                <div className="report-meta">
                  <span>{report.researcher}</span>
                  <span>{report.submittedAt}</span>
                </div>
              </div>

              <span
                className={`status-badge ${report.status.toLowerCase()}`}
              >
                {report.status}
              </span>

            </div>

            <div className="company-report-info">

              <div>
                <span className="info-label">Recompensa</span>

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

            <div className="company-actions">

              {report.status === 'VALIDATED' && (
                <button
                  className="primary-button"
                  onClick={() => payReward(report.id)}
                >
                  Pagar recompensa
                </button>
              )}

              {report.status === 'PAID' && (
                <button
                  className="primary-button"
                  onClick={() => markRemediated(report.id)}
                >
                  Marcar como remediada
                </button>
              )}

              {report.status === 'REMEDIATED' && (
                <span className="waiting-message">
                  Esperando verificación final
                </span>
              )}

              {report.status === 'VERIFIED' && (
                <span className="completed-message">
                  ✓ Proceso completado
                </span>
              )}

            </div>

          </div>
        ))}

      </div>

    </div>
  )
}

export default Company