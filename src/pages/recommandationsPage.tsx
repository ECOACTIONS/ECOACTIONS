import { useState } from 'react'
import ChatbotSection from './chatbotSection' // Ajuste le chemin selon ton dossier

interface Engagement {
  id: string
  title: string
  metric: string
  carbonSaving: number
  category: string
}

export default function RecommandationsPage() {
  const userAnswersMock = {
  transportType: 'diesel-large',
  motoTaxiUsage: 'intensif',
  climatisation: 'oui',
  factureElectricite: 'high',
  alimentationType: 'import-heavy',
  dechetsGestion: 'incineration'
}
  const [darkMode, setDarkMode] = useState<boolean>(true)
  const [selectedActions, setSelectedActions] = useState<string[]>([])

  const engagements: Engagement[] = [
    {
      id: 'marche',
      title: "Marcher 5 km par semaine au lieu de prendre une moto-taxi",
      metric: "Moins de trajets < 1 km",
      carbonSaving: 12,
      category: "Mobilité"
    },
    {
      id: 'transit',
      title: "Privilégier le taxi collectif sur les grands axes",
      metric: "Transit partagé",
      carbonSaving: 18,
      category: "Mobilité"
    },
    {
      id: 'clim',
      title: "Réguler la climatisation à 24°C et couper en absence",
      metric: "Optimisation Eneo",
      carbonSaving: 30,
      category: "Énergie"
    },
    {
      id: 'led',
      title: "Passer à 100% d'éclairage LED basse consommation",
      metric: "Efficacité domestique",
      carbonSaving: 15,
      category: "Énergie"
    },
    {
      id: 'local',
      title: "Substituer deux repas importés par des vivres frais du marché",
      metric: "Circuit court",
      carbonSaving: 25,
      category: "Alimentation"
    },
    {
      id: 'dechets',
      title: "Stopper l'incinération des plastiques et trier les déchets",
      metric: "Zéro combustion",
      carbonSaving: 35,
      category: "Résidus"
    }
  ]

  const toggleAction = (id: string) => {
    setSelectedActions(prev => 
      prev.includes(id) ? prev.filter(item => item !== id) : [...prev, id]
    )
  }

  const totalSaving = engagements
    .filter(action => selectedActions.includes(action.id))
    .reduce((sum, action) => sum + action.carbonSaving, 0)

  const progress = Math.min((totalSaving / 100) * 100, 100)

  return (
    <div className={`min-h-screen font-sans antialiased transition-colors duration-500 tracking-tight flex flex-col ${
      darkMode ? 'bg-[#090d16] text-[#f8fafc]' : 'bg-[#f8fafc] text-[#0f172a]'
    }`}>
      
      {/* TOPBAR NAVIGATION */}
      <header className={`border-b px-6 py-4 flex justify-between items-center backdrop-blur-md sticky top-0 z-50 ${
        darkMode ? 'bg-[#090d16]/80 border-[#1e293b]' : 'bg-[#f8fafc]/80 border-[#e2e8f0]'
      }`}>
        <div className="flex items-center gap-3">
          <div className="w-5 h-5 rounded bg-emerald-600 flex items-center justify-center">
            <div className="w-2 h-2 rounded-sm bg-white"></div>
          </div>
          <span className="text-xs font-bold uppercase tracking-widest text-emerald-600 dark:text-emerald-500">
            EcoImpact AI / Plan d'Action
          </span>
        </div>
        <button
          type="button"
          onClick={() => setDarkMode(!darkMode)}
          className={`text-[10px] font-bold tracking-widest px-3 py-1.5 rounded border transition-all duration-300 ${
            darkMode ? 'bg-[#131c2e] border-[#1e293b] text-[#94a3b8]' : 'bg-white border-[#e2e8f0] text-[#64748b]'
          }`}
        >
          {darkMode ? 'LIGHT' : 'DARK'}
        </button>
      </header>

      {/* TWO-COLUMN GRID ARCHITECTURE */}
      <main className="max-w-6xl w-full mx-auto px-4 py-8 md:py-16 flex-1 flex flex-col gap-12">
        
        {/* TOP ROW: DASHBOARD (2 COLUMNS) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* LEFT COLUMN: THE REAL-TIME IMPACT ENGINE */}
          <div className="lg:col-span-5 space-y-6">
            <div>
              <span className={`text-[10px] font-bold uppercase tracking-widest ${darkMode ? 'text-[#475569]' : 'text-[#94a3b8]'}`}>
                Analyse d'impact en direct
              </span>
              <h1 className="text-2xl sm:text-3xl font-black tracking-tight mt-1 leading-tight">
                Construisez votre plan de transition.
              </h1>
              <p className="text-xs mt-2 leading-relaxed text-[#64748b]">
                Cochez les actions que vous êtes prêt à appliquer. Observez la réduction de votre empreinte se calculer instantanément.
              </p>
            </div>

            {/* MASSIVE SCORE INDICATOR CARD */}
            <div className={`border rounded-2xl p-6 transition-all duration-300 ${
              darkMode ? 'bg-[#0d1321] border-[#1e293b]' : 'bg-white border-[#e2e8f0] shadow-sm'
            }`}>
              <div className="mb-6">
                <span className={`text-[10px] font-bold uppercase tracking-widest ${darkMode ? 'text-[#475569]' : 'text-[#94a3b8]'}`}>
                  CO₂ Évité Cumulé
                </span>
                <div className="text-5xl font-mono font-black text-emerald-500 mt-2 flex items-baseline gap-1">
                  -{totalSaving} 
                  <span className="text-xs font-sans font-bold tracking-normal text-[#64748b]">
                    kg / mois
                  </span>
                </div>
              </div>

              {/* RADICAL PROGRESS BAR */}
              <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest">
                  <span className={darkMode ? 'text-[#475569]' : 'text-[#94a3b8]'}>Objectif Minimum</span>
                  <span className="text-emerald-500 font-mono">{Math.round(progress)}%</span>
                </div>
                <div className={`h-2.5 w-full rounded-full overflow-hidden relative ${darkMode ? 'bg-[#131c2e]' : 'bg-[#e2e8f0]'}`}>
                  <div 
                    className="h-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-500 ease-out shadow-[0_0_12px_#10b981]"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            </div>

            {/* ACTION BUTTON */}
            <button
              type="button"
              onClick={() => alert('Plan de transition validé.')}
              disabled={selectedActions.length === 0}
              className={`w-full text-xs font-bold uppercase tracking-widest py-4 rounded-xl transition-all active:scale-[0.99] text-center ${
                selectedActions.length === 0
                  ? 'opacity-20 cursor-not-allowed bg-[#131c2e] text-[#475569] border border-[#1e293b]'
                  : (darkMode ? 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-500/10' : 'bg-[#0f172a] hover:bg-[#1e293b] text-white')
              }`}
            >
              Enregistrer mes engagements ({selectedActions.length})
            </button>
          </div>

          {/* RIGHT COLUMN: INTERACTIVE CARDS SECTION */}
          <div className="lg:col-span-7 space-y-3">
            {engagements.map(action => {
              const isChecked = selectedActions.includes(action.id)
              return (
                <div
                  key={action.id}
                  onClick={() => toggleAction(action.id)}
                  className={`p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 flex items-center justify-between gap-4 group ${
                    isChecked
                      ? (darkMode ? 'border-emerald-500 bg-[#0e1726]' : 'border-emerald-600 bg-emerald-50/30')
                      : (darkMode ? 'border-[#1e293b] bg-[#0d1321]/40 hover:border-[#334155]' : 'border-[#e2e8f0] bg-white hover:border-[#cbd5e1]')
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-5 h-5 rounded border flex items-center justify-center transition-all flex-shrink-0 ${
                      isChecked ? 'border-emerald-500 bg-emerald-500 text-white' : (darkMode ? 'border-[#334155] bg-[#090d16]' : 'border-[#cbd5e1] bg-white')
                    }`}>
                      {isChecked && (
                        <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3.5">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                      )}
                    </div>

                    <div>
                      <h3 className={`text-sm font-semibold tracking-tight leading-snug transition-colors ${
                        isChecked ? 'text-white dark:text-white' : (darkMode ? 'text-[#94a3b8]' : 'text-[#334155]')
                      }`}>
                        {action.title}
                      </h3>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-[9px] font-mono font-bold uppercase tracking-wider text-[#475569]">
                          {action.metric}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="text-right flex-shrink-0">
                    <span className={`text-xs font-mono font-bold tracking-tight ${isChecked ? 'text-emerald-400' : 'text-emerald-600/70'}`}>
                      -{action.carbonSaving}kg
                    </span>
                  </div>
                </div>
              )
            })}
          </div>

        </div>

        {/* BOTTOM ROW: CHATBOT COMPLETELY SEPARATED HERE */}
        <div className="w-full pt-4 border-t border-dashed border-[#1e293b]">
          <div className="mb-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-500">
              Des interrogations sur vos résultats ? Discutez avec notre IA
            </h3>
          </div>
          <ChatbotSection userContext={userAnswersMock} />
        </div>

      </main>
      {/* BALANCING SYSTEM FOOTER */}
      <footer className={`border-t text-[9px] font-mono text-center py-4 tracking-widest mt-12 ${
        darkMode ? 'border-[#1e293b] text-[#223147]' : 'border-[#e2e8f0] text-[#94a3b8]'
      }`}>
        TRANSITION FRAMEWORK // REALTIME DATA INTERACTION
      </footer>

    </div>
  )
}