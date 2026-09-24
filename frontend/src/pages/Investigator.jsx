import { useState } from 'react'
import ReportTimeline from '../components/ReportTimeline'

function Investigator({ reports, setReports }) {
  const [showForm, setShowForm] = useState(false)
  const [selectedReportId, setSelectedReportId] = useState(null)

  const [formData, setFormData] = useState({
    title: '',
    company: '',
    severity: 'Medium',
    description: '',
  })

  const researcher = '0xSamResearcher'

  const myReports = reports.filter(
    (report) => report.researcher === researcher
  )

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData({
      ...formData,
      [name]: value,
    })
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    const newReport = {
      id: `PP-${String(reports.length + 1).padStart(3, '0')}`,
      title: formData.title,
      company: formData.company,
      severity: formData.severity,
      description: formData.description,
      status: 'SUBMITTED',
      researcher,
      submittedAt: '23 Sep 2026',
      reward: null,
      evidenceHash: 'Pendiente de registro',
      transactionHash: null,
    }

    setReports([newReport, ...reports])

    setFormData({
      title: '',
      company: '',
      severity: 'Medium',
      description: '',
    })

    setShowForm(false)
  }

  return (
    <div className="investigator-page">

      <div className="page-heading">
        <div>
          <p className="section-label">Investigador</p>

          <h2>Mis reportes</h2>

          <p className="section-description">
            Consulta tus vulnerabilidades reportadas y su estado actual.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancelar' : '+ Nuevo reporte'}
        </button>
      </div>

      {showForm && (
        <form
          className="report-form"
          onSubmit={handleSubmit}
        >
          <div className="form-header">
            <h3>Reportar vulnerabilidad</h3>

            <p>
              Registra la información necesaria para iniciar el proceso
              de validación.
            </p>
          </div>

          <div className="form-grid">

            <div className="form-group">
              <label>Título</label>

              <input
                type="text"
                name="title"
                placeholder="Ej. Exposición de información sensible"
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Empresa</label>

              <input
                type="text"
                name="company"
                placeholder="Ej. NovaPay"
                value={formData.company}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label>Severidad</label>

              <select
                name="severity"
                value={formData.severity}
                onChange={handleChange}
              >
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>

            <div className="form-group full-width">
              <label>Descripción y evidencia</label>

              <textarea
                name="description"
                rows="5"
                placeholder="Describe la vulnerabilidad, cómo reproducirla y la evidencia encontrada..."
                value={formData.description}
                onChange={handleChange}
                required
              />
            </div>

          </div>

          <div className="form-actions">
            <button
              type="submit"
              className="primary-button"
            >
              Enviar reporte
            </button>
          </div>
        </form>
      )}

      <div className="researcher-reports">

        {myReports.map((report) => (
          <div key={report.id}>

            <div className="researcher-report-card">

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
                  <span>{report.company}</span>
                  <span>{report.submittedAt}</span>
                </div>
              </div>

              <div className="report-card-actions">

                <span
                  className={`status-badge ${report.status.toLowerCase()}`}
                >
                  {report.status}
                </span>

                <button
                  className="secondary-button"
                  onClick={() =>
                    setSelectedReportId(
                      selectedReportId === report.id
                        ? null
                        : report.id
                    )
                  }
                >
                  {selectedReportId === report.id
                    ? 'Ocultar detalle'
                    : 'Ver detalle'}
                </button>

              </div>

            </div>

            {selectedReportId === report.id && (
              <ReportTimeline report={report} />
            )}

          </div>
        ))}

      </div>

    </div>
  )
}

export default Investigator