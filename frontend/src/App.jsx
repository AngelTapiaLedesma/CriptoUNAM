import { useEffect, useState } from 'react'
import './App.css'

import Dashboard from './pages/Dashboard'
import Investigator from './pages/Investigator'
import Triager from './pages/Triager'
import Company from './pages/Company'

// IMPORTANTE: Importamos tu cliente de API real
import { getReports } from './services/api' 

function App() {
  const [activeSection, setActiveSection] = useState('dashboard')

  // Iniciamos el estado vacío, esperando los datos reales
  const [reports, setReports] = useState([])

  // Este useEffect se ejecuta una sola vez al abrir la app
  // y va a buscar los datos a tu FastAPI (http://127.0.0.1:8000/reports)
  useEffect(() => {
    const fetchRealData = async () => {
      try {
        const data = await getReports()
        setReports(data)
      } catch (error) {
        console.error("Error cargando DB desde backend:", error)
      }
    }
    fetchRealData()
  }, [])

  const resetDemo = async () => {
    // En lugar de borrar local storage, forzamos una recarga desde el backend
    try {
      const data = await getReports()
      setReports(data)
      setActiveSection('dashboard')
    } catch (error) {
      console.error("Error al recargar demo:", error)
    }
  }

  const sections = [
    { id: 'dashboard', name: 'Dashboard', icon: '⌂' },
    { id: 'researcher', name: 'Investigador', icon: '⌕' },
    { id: 'triager', name: 'Triager', icon: '✓' },
    { id: 'company', name: 'Empresa', icon: '▦' },
  ]

  const titles = {
    dashboard: 'Dashboard',
    researcher: 'Portal del investigador',
    triager: 'Panel de triage',
    company: 'Panel de empresa',
  }

  return (
    <div className="app-shell">

      <aside className="sidebar">

        <div className="brand">
          <div className="brand-icon">P</div>

          <div>
            <h2>PatchProof</h2>
            <span>Bug Bounty Platform</span>
          </div>
        </div>

        <nav className="navigation">

          {sections.map((section) => (
            <button
              key={section.id}
              className={
                activeSection === section.id
                  ? 'nav-item active'
                  : 'nav-item'
              }
              onClick={() => setActiveSection(section.id)}
            >
              <span className="nav-icon">
                {section.icon}
              </span>

              {section.name}
            </button>
          ))}

        </nav>

        <div className="network-status">
          <span className="status-dot"></span>

          <div>
            <strong>Stellar Testnet</strong>
            <p>Red de pruebas</p>
          </div>
        </div>

      </aside>

      <main className="main-content">

        <header className="topbar">

          <div>
            <p className="eyebrow">PATCHPROOF</p>
            <h1>{titles[activeSection]}</h1>
          </div>

          <div className="topbar-actions">

            <button
              className="reset-button"
              onClick={resetDemo}
            >
              Recargar datos
            </button>

            <div className="user-profile">

              <div className="avatar">
                SM
              </div>

              <div>
                <strong>Demo User</strong>
                <span>Hackathon</span>
              </div>

            </div>

          </div>

        </header>

        <section className="page-content">

          {activeSection === 'dashboard' && (
            <Dashboard reports={reports} />
          )}

          {activeSection === 'researcher' && (
            <Investigator
              reports={reports}
              setReports={setReports}
            />
          )}

          {activeSection === 'triager' && (
            <Triager
              reports={reports}
              setReports={setReports}
            />
          )}

          {activeSection === 'company' && (
            <Company
              reports={reports}
              setReports={setReports}
            />
          )}

        </section>

      </main>

    </div>
  )
}

export default App