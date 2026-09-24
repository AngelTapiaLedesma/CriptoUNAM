import { useEffect, useState } from 'react'
import './App.css'

import Dashboard from './pages/Dashboard'
import Investigator from './pages/Investigator'
import Triager from './pages/Triager'
import Company from './pages/Company'

import { mockReports } from './data/mockReports'

function App() {
  const [activeSection, setActiveSection] = useState('dashboard')

  const [reports, setReports] = useState(() => {
    const savedReports = localStorage.getItem('patchproof-reports')

    return savedReports
      ? JSON.parse(savedReports)
      : mockReports
  })

  useEffect(() => {
    localStorage.setItem(
      'patchproof-reports',
      JSON.stringify(reports)
    )
  }, [reports])

  const resetDemo = () => {
    localStorage.removeItem('patchproof-reports')
    setReports(mockReports)
    setActiveSection('dashboard')
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
              Reiniciar demo
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