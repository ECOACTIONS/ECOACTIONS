import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/homePage' // ou HomePage si renommé
import LoginPage from './pages/loginPage'
import RegisterPage from './pages/registerPage'
import CalculateurPage from './pages/calculateurPage'

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Route pour la page d'accueil (la racine /) */}
        <Route path="/" element={<HomePage />} />
        
        {/* Autres routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/calculer" element={<CalculateurPage />} />
      </Routes>
    </Router>
  )
}