import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import '@pollar/react/styles.css'

// 1. Importamos el proveedor del SDK de Pollar
import { PollarProvider } from '@pollar/react'

// 2. Leemos la llave pública de tu archivo .env
const pollarApiKey = import.meta.env.VITE_POLLAR_PUBLISHABLE_KEY

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* 3. Envolvemos la app inyectando la llave */}
    <PollarProvider client={{ apiKey: pollarApiKey }}>
      <App />
    </PollarProvider>
  </StrictMode>,
)