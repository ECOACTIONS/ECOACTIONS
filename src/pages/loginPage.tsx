import { useState, type FormEvent } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'

export default function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  const from = (location.state as { from?: string } | null)?.from || '/'

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    localStorage.setItem('authUser', email)
    localStorage.setItem('authToken', 'demo-token')
    navigate(from, { replace: true })
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4 font-sans">
      <div className="bg-white rounded-2xl p-8 w-full max-w-md border border-slate-100 shadow-xl shadow-slate-100/50">

        {/* Logo & Header */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 bg-emerald-600 rounded-xl flex items-center justify-center mb-3 shadow-md shadow-emerald-600/20">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.5A7 7 0 0111 20z" />
            </svg>
          </div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">EcoImpact AI</h1>
          <p className="text-sm text-slate-500 mt-2 text-center">
            Accédez à votre tableau de bord environnemental
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          
          {/* Email */}
          <div>
            <label className="text-xs font-semibold text-slate-700 mb-1.5 block">Adresse email</label>
            <div className="flex items-center border border-slate-200 rounded-xl px-3.5 py-2.5 gap-2.5 focus-within:border-emerald-600 focus-within:ring-2 focus-within:ring-emerald-600/10 transition-all">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <input
                type="email"
                required
                placeholder="nom@entreprise.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="flex-1 text-sm outline-none text-slate-800 bg-transparent placeholder:text-slate-400"
              />
            </div>
          </div>

          {/* Mot de passe */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-slate-700">Mot de passe</label>
              <Link to="/forgot-password" className="text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:underline transition-colors">
                Mot de passe oublié ?
              </Link>
            </div>
            <div className="flex items-center border border-slate-200 rounded-xl px-3.5 py-2.5 gap-2.5 focus-within:border-emerald-600 focus-within:ring-2 focus-within:ring-emerald-600/10 transition-all">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input
                type={showPassword ? 'text' : 'password'}
                required
                placeholder="••••••••"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="flex-1 text-sm outline-none text-slate-800 bg-transparent placeholder:text-slate-400"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-slate-400 hover:text-slate-600 transition-colors focus:outline-none"
              >
                {showPassword ? (
                  /* Icône Œil barré (Masquer) */
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18" />
                  </svg>
                ) : (
                  /* Icône Œil (Afficher) */
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {/* Bouton de connexion */}
          <button
            type="submit"
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3 rounded-xl mt-2 transition-colors duration-200 shadow-md shadow-emerald-600/10 active:scale-[0.99]"
          >
            Se connecter
          </button>
        </form>

        {/* Séparateur */}
        <div className="flex items-center gap-3 my-6">
          <div className="flex-1 h-px bg-slate-100" />
          <span className="text-xs font-medium text-slate-400 whitespace-nowrap">Ou continuer avec</span>
          <div className="flex-1 h-px bg-slate-100" />
        </div>

        {/* Boutons d'authentification sociale */}
        <div className="flex gap-3">
          <button className="flex-1 flex items-center justify-center gap-2 border border-slate-200 rounded-xl py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-200">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            Google
          </button>
          
          <button className="flex-1 flex items-center justify-center gap-2 border border-slate-200 rounded-xl py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-200">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 4.17c.66-.81 1.11-1.93.99-3.06-1 .04-2.21.67-2.93 1.49-.62.69-1.16 1.84-1.01 2.96 1.12.09 2.27-.57 2.95-1.39z" />
            </svg>
            Apple
          </button>
        </div>

        {/* Lien de redirection */}
        <p className="text-center text-xs text-slate-500 mt-6">
          Pas encore de compte ?{' '}
          <Link to="/register" state={{ from }} className="text-emerald-600 font-semibold hover:text-emerald-700 hover:underline transition-colors">
            S'inscrire
          </Link>
        </p>
      </div>
    </div>
  )
}