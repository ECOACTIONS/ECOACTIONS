import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function RegisterPage() {
  const [nom, setNom] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')

  const handleSubmit = (e: any) => { // 👈 On dit à TS de ne pas vérifier le type
  e.preventDefault()
  
  if (password !== confirm) {
    alert("Les mots de passe ne correspondent pas.")
    return
  }

  console.log({ nom, email, password, confirm })
}

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4 family-sans">
      <div className="bg-white rounded-2xl p-8 w-full max-w-md border border-slate-100 shadow-xl shadow-slate-100/50">

        {/* Logo & Header */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 bg-emerald-600 rounded-xl flex items-center justify-center mb-3 shadow-md shadow-emerald-600/20">
            {/* Icône de feuille abstraite en SVG */}
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.5A7 7 0 0111 20z" />
            </svg>
          </div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">EcoImpact AI</h1>
          <p className="text-sm text-slate-500 mt-2 text-center">
            Rejoignez la communauté éco-responsable du Cameroun
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          
          {/* Nom */}
          <div>
            <label className="text-xs font-semibold text-slate-700 mb-1.5 block">Nom complet</label>
            <div className="flex items-center border border-slate-200 rounded-xl px-3.5 py-2.5 gap-2.5 focus-within:border-emerald-600 focus-within:ring-2 focus-within:ring-emerald-600/10 transition-all">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <input
                type="text"
                required
                placeholder="Ex: Jean Dupont"
                value={nom}
                onChange={e => setNom(e.target.value)}
                className="flex-1 text-sm outline-none text-slate-800 bg-transparent placeholder:text-slate-400"
              />
            </div>
          </div>

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
                placeholder="nom@exemple.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="flex-1 text-sm outline-none text-slate-800 bg-transparent placeholder:text-slate-400"
              />
            </div>
          </div>

          {/* Mot de passe */}
          <div>
            <label className="text-xs font-semibold text-slate-700 mb-1.5 block">Mot de passe</label>
            <div className="flex items-center border border-slate-200 rounded-xl px-3.5 py-2.5 gap-2.5 focus-within:border-emerald-600 focus-within:ring-2 focus-within:ring-emerald-600/10 transition-all">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="flex-1 text-sm outline-none text-slate-800 bg-transparent placeholder:text-slate-400"
              />
            </div>
          </div>

          {/* Confirmer le mot de passe */}
          <div>
            <label className="text-xs font-semibold text-slate-700 mb-1.5 block">Confirmer le mot de passe</label>
            <div className="flex items-center border border-slate-200 rounded-xl px-3.5 py-2.5 gap-2.5 focus-within:border-emerald-600 focus-within:ring-2 focus-within:ring-emerald-600/10 transition-all">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input
                type="password"
                required
                placeholder="••••••••"
                value={confirm}
                onChange={e => setConfirm(e.target.value)}
                className="flex-1 text-sm outline-none text-slate-800 bg-transparent placeholder:text-slate-400"
              />
            </div>
          </div>

          {/* Bouton de soumission */}
          <button
            type="submit"
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3 rounded-xl mt-2 transition-colors duration-200 shadow-md shadow-emerald-600/10 active:scale-[0.99]"
          >
            Créer mon compte
          </button>
        </form>

        {/* Lien de redirection */}
        <p className="text-center text-xs text-slate-500 mt-6">
          Déjà inscrit ?{' '}
          <Link to="/login" className="text-emerald-600 font-semibold hover:text-emerald-700 hover:underline transition-colors">
            Se connecter
          </Link>
        </p>
      </div>
    </div>
  )
}