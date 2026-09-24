const API_URL =
  import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function getReports() {
  const response = await fetch(`${API_URL}/reports`)

  if (!response.ok) {
    throw new Error('No se pudieron obtener los reportes')
  }

  return response.json()
}

export async function createReport(reportData) {
  const response = await fetch(`${API_URL}/reports`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(reportData),
  })

  if (!response.ok) {
    throw new Error('No se pudo crear el reporte')
  }

  return response.json()
}

export async function updateReportStatus(reportId, status) {
  const response = await fetch(
    `${API_URL}/reports/${reportId}/status`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status }),
    }
  )

  if (!response.ok) {
    throw new Error('No se pudo actualizar el reporte')
  }

  return response.json()
}