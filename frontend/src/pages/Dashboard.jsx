

function Dashboard({ reports }) {
  const totalReports = reports.length

  const submittedReports = reports.filter(
    (report) => report.status === 'SUBMITTED'
  ).length

  const verifiedReports = reports.filter(
    (report) => report.status === 'VERIFIED'
  ).length

  const totalRewards = reports.reduce(
    (total, report) => total + (report.reward || 0),
    0
  )

  return (
    <div className="dashboard">

      <div className="welcome-section">
        <div>
          <p className="section-label">Resumen general</p>
          <h2>Actividad de vulnerabilidades</h2>
          <p className="section-description">
            Seguimiento de reportes, validaciones y recompensas registradas
            en PatchProof.
          </p>
        </div>
      </div>

      <div className="stats-grid">

        <div className="stat-card">
          <span className="stat-label">Reportes totales</span>
          <strong>{totalReports}</strong>
          <span className="stat-detail">Vulnerabilidades registradas</span>
        </div>

        <div className="stat-card">
          <span className="stat-label">Pendientes de triage</span>
          <strong>{submittedReports}</strong>
          <span className="stat-detail">Esperando validación</span>
        </div>

        <div className="stat-card">
          <span className="stat-label">Verificados</span>
          <strong>{verifiedReports}</strong>
          <span className="stat-detail">Proceso completado</span>
        </div>

        <div className="stat-card">
          <span className="stat-label">Recompensas</span>
          <strong>{totalRewards} XLM</strong>
          <span className="stat-detail">Valor simulado</span>
        </div>

      </div>

      <div className="reports-panel">

        <div className="panel-header">
          <div>
            <p className="section-label">Última actividad</p>
            <h3>Reportes recientes</h3>
          </div>

          <span className="report-count">
            {totalReports} reportes
          </span>
        </div>

        <div className="table-wrapper">
          <table className="reports-table">

            <thead>
              <tr>
                <th>ID</th>
                <th>Vulnerabilidad</th>
                <th>Empresa</th>
                <th>Severidad</th>
                <th>Estado</th>
                <th>Recompensa</th>
              </tr>
            </thead>

            <tbody>
              {reports.map((report) => (
                <tr key={report.id}>
                  <td className="report-id">{report.id}</td>

                  <td>
                    <strong>{report.title}</strong>
                    <span className="report-date">
                      {report.submittedAt}
                    </span>
                  </td>

                  <td>{report.company}</td>

                  <td>
                    <span
                      className={`severity-badge ${report.severity.toLowerCase()}`}
                    >
                      {report.severity}
                    </span>
                  </td>

                  <td>
                    <span
                      className={`status-badge ${report.status.toLowerCase()}`}
                    >
                      {report.status}
                    </span>
                  </td>

                  <td>
                    {report.reward
                      ? `${report.reward} XLM`
                      : 'Pendiente'}
                  </td>
                </tr>
              ))}
            </tbody>

          </table>
        </div>

      </div>

    </div>
  )
}

export default Dashboard