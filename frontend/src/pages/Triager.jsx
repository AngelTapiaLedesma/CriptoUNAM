function Triager({ reports, setReports }) {
  const pendingReports = reports.filter(
    (report) => report.status === 'SUBMITTED'
  )

  const remediationReports = reports.filter(
    (report) => report.status === 'REMEDIATED'
  )

  const validateReport = (reportId) => {
    const updatedReports = reports.map((report) =>
      report.id === reportId
        ? { ...report, status: 'VALIDATED' }
        : report
    )

    setReports(updatedReports)
  }

  const verifyReport = (reportId) => {
    const updatedReports = reports.map((report) =>
      report.id === reportId
        ? { ...report, status: 'VERIFIED' }
        : report
    )

    setReports(updatedReports)
  }

  return (
    <div className="triager-page">

      <div className="page-heading">
        <div>
          <p className="section-label">Triager</p>
          <h2>Revisión de vulnerabilidades</h2>

          <p className="section-description">
            Valida nuevos reportes y comprueba las vulnerabilidades
            que fueron marcadas como remediadas.
          </p>
        </div>
      </div>

      <div className="triage-section">

        <div className="triage-section-header">
          <div>
            <p className="section-label">Triage inicial</p>
            <h3>Reportes pendientes</h3>
          </div>

          <div className="pending-counter">
            {pendingReports.length} pendientes
          </div>
        </div>

        {pendingReports.length === 0 ? (
          <div className="empty-state">
            <span>✓</span>
            <h3>No hay reportes pendientes</h3>
            <p>Todos los reportes enviados ya fueron revisados.</p>
          </div>
        ) : (
          <div className="triage-list">

            {pendingReports.map((report) => (
              <div className="triage-card" key={report.id}>

                <div className="triage-card-header">
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
                  </div>

                  <span className="status-badge submitted">
                    SUBMITTED
                  </span>
                </div>

                <div className="triage-information">

                  <div>
                    <span className="info-label">Empresa</span>
                    <strong>{report.company}</strong>
                  </div>

                  <div>
                    <span className="info-label">Investigador</span>
                    <strong>{report.researcher}</strong>
                  </div>

                  <div>
                    <span className="info-label">Fecha</span>
                    <strong>{report.submittedAt}</strong>
                  </div>

                </div>

                {report.description && (
                  <div className="report-description">
                    <span className="info-label">
                      Descripción y evidencia
                    </span>

                    <p>{report.description}</p>
                  </div>
                )}

                <div className="triage-actions">
                  <button
                    className="primary-button"
                    onClick={() => validateReport(report.id)}
                  >
                    ✓ Validar reporte
                  </button>
                </div>

              </div>
            ))}

          </div>
        )}

      </div>

      <div className="triage-section">

        <div className="triage-section-header">
          <div>
            <p className="section-label">Verificación final</p>
            <h3>Remediaciones por comprobar</h3>
          </div>

          <div className="pending-counter">
            {remediationReports.length} pendientes
          </div>
        </div>

        {remediationReports.length === 0 ? (
          <div className="empty-state">
            <span>✓</span>
            <h3>No hay remediaciones pendientes</h3>
            <p>
              No existen vulnerabilidades esperando verificación final.
            </p>
          </div>
        ) : (
          <div className="triage-list">

            {remediationReports.map((report) => (
              <div className="triage-card verification-card" key={report.id}>

                <div className="triage-card-header">

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
                  </div>

                  <span className="status-badge remediated">
                    REMEDIATED
                  </span>

                </div>

                <div className="triage-information">

                  <div>
                    <span className="info-label">Empresa</span>
                    <strong>{report.company}</strong>
                  </div>

                  <div>
                    <span className="info-label">Investigador</span>
                    <strong>{report.researcher}</strong>
                  </div>

                  <div>
                    <span className="info-label">Recompensa</span>
                    <strong>
                      {report.reward
                        ? `${report.reward} XLM`
                        : 'Sin recompensa'}
                    </strong>
                  </div>

                </div>

                <div className="verification-message">
                  La empresa reportó que la vulnerabilidad fue corregida.
                  Comprueba nuevamente el hallazgo antes de cerrar el reporte.
                </div>

                <div className="triage-actions">
                  <button
                    className="primary-button"
                    onClick={() => verifyReport(report.id)}
                  >
                    ✓ Confirmar corrección
                  </button>
                </div>

              </div>
            ))}

          </div>
        )}

      </div>

    </div>
  )
}

export default Triager