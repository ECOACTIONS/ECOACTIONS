import { useState, FormEvent } from 'react'

interface FormData {
  transportType: string
  motoTaxiUsage: string
  climatisation: string
  factureElectricite: string
  alimentationType: string
  dechetsGestion: string
}

export default function CalculateurPage() {
  const [step, setStep] = useState<number>(1)
  const [darkMode, setDarkMode] = useState<boolean>(false)
  const [formData, setFormData] = useState<FormData>({
    transportType: '',
    motoTaxiUsage: '',
    climatisation: '',
    factureElectricite: '',
    alimentationType: '',
    dechetsGestion: ''
  })

  const updateField = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleNext = () => {
    if (step < 5) setStep(prev => prev + 1)
  }

  const handlePrev = () => {
    if (step > 1) setStep(prev => prev - 1)
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    console.log('Payload:', formData)
  }

  const progressPercentage = (step / 5) * 100

  return (
    <div className={`min-h-screen font-sans antialiased transition-colors duration-500 tracking-tight flex flex-col justify-between ${
      darkMode ? 'bg-[#090d16] text-[#f8fafc]' : 'bg-[#f8fafc] text-[#0f172a]'
    }`}>
      
      {/* HEADER TOP-BAR */}
      <header className={`border-b px-6 py-4 flex justify-between items-center backdrop-blur-md sticky top-0 z-50 ${
        darkMode ? 'bg-[#090d16]/80 border-[#1e293b]' : 'bg-[#f8fafc]/80 border-[#e2e8f0]'
      }`}>
        <div className="flex items-center gap-3">
          <div className="w-6 h-6 rounded bg-emerald-600 flex items-center justify-center shadow-lg shadow-emerald-600/20">
            <div className="w-2 h-2 rounded-sm bg-white"></div>
          </div>
          <span className="text-xs font-semibold uppercase tracking-widest text-emerald-600 dark:text-emerald-500">
            <a href="#homePage">EcoImpact AI</a>
          </span>
        </div>
        
        <button
          type="button"
          onClick={() => setDarkMode(!darkMode)}
          className={`text-xs font-medium tracking-wide px-3.5 py-1.5 rounded-md border transition-all duration-300 ${
            darkMode 
              ? 'bg-[#131c2e] border-[#1e293b] text-[#94a3b8] hover:text-white hover:border-[#334155]' 
              : 'bg-white border-[#e2e8f0] text-[#64748b] hover:text-[#0f172a] hover:border-[#cbd5e1]'
          }`}
        >
          {darkMode ? 'clair' : 'sombre'}
        </button>
      </header>

      {/* CORE FORM CONTAINER */}
      <main className="max-w-xl w-full mx-auto px-4 py-12 md:py-20 flex-1 flex flex-col justify-center">
        
        {/* LASER PROGRESSION INDICATOR */}
        <div className="mb-10 w-full">
          <div className="flex justify-between items-baseline mb-3">
            <span className={`text-[10px] font-bold uppercase tracking-widest ${darkMode ? 'text-[#475569]' : 'text-[#94a3b8]'}`}>
              Metric Sequence / 0{step}
            </span>
            <span className={`text-xs font-mono font-bold ${darkMode ? 'text-emerald-400' : 'text-emerald-600'}`}>
              {Math.round(progressPercentage)}%
            </span>
          </div>
          <div className={`h-[3px] w-full rounded-full relative overflow-hidden ${darkMode ? 'bg-[#131c2e]' : 'bg-[#e2e8f0]'}`}>
            <div 
              className="h-full bg-emerald-500 transition-all duration-500 ease-in-out shadow-[0_0_8px_#10b981]"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>

        {/* STEP CONTROLLER CONTAINER */}
        <form onSubmit={handleSubmit} className="w-full">
          
          {/* STEP 1: TRANSPORT MOTORISÉ */}
          {step === 1 && (
            <div className="space-y-6 animate-[fadeIn_0.4s_ease-out]">
              <div>
                <h2 className="text-2xl font-bold tracking-tight mb-2">Structure de mobilité principale</h2>
                <p className={`text-xs ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>Sélectionnez la configuration mécanique correspondant à votre véhicule usuel au Cameroun.</p>
              </div>
              <div className="grid grid-cols-1 gap-3">
                {[
                  { id: 'none', title: 'Transport en commun', desc: 'Usage exclusif des bus de ligne et taxis collectifs urbains.' },
                  { id: 'moto', title: 'Deux-roues Motorisé Personnel', desc: 'Moto personnelle ou scooter de cylindrée standard.' },
                  { id: 'essence-small', title: 'Motorisation Essence Légère', desc: 'Véhicule citadin de faible litrage ou berline compacte.' },
                  { id: 'diesel-large', title: 'Châssis Lourd Diesel', desc: 'SUV, Pick-up double cabine ou véhicule utilitaire à forte charge.' },
                ].map(opt => (
                  <div 
                    key={opt.id}
                    onClick={() => updateField('transportType', opt.id)}
                    className={`p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 relative overflow-hidden group ${
                      formData.transportType === opt.id 
                        ? (darkMode ? 'border-emerald-500 bg-[#0e1726]' : 'border-emerald-600 bg-emerald-50/30') 
                        : (darkMode ? 'border-[#1e293b] bg-[#0d1321] hover:border-[#334155]' : 'border-[#e2e8f0] bg-white hover:border-[#cbd5e1]')
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-sm font-semibold tracking-tight">{opt.title}</h4>
                        <p className={`text-xs mt-1 leading-relaxed ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>{opt.desc}</p>
                      </div>
                      <div className={`w-3.5 h-3.5 rounded-full border flex items-center justify-center transition-all mt-0.5 ${
                        formData.transportType === opt.id ? 'border-emerald-500 bg-emerald-500' : 'border-[#475569]'
                      }`}>
                        {formData.transportType === opt.id && <div className="w-1.5 h-1.5 rounded-full bg-white"></div>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* STEP 2: CADENCE MOTO-TAXI */}
          {step === 2 && (
            <div className="space-y-6 animate-[fadeIn_0.4s_ease-out]">
              <div>
                <h2 className="text-2xl font-bold tracking-tight mb-2">Fréquentation du réseau Moto-Taxi</h2>
                <p className={`text-xs ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>Volume d'utilisation estimé des réseaux de transporteurs par deux-roues.</p>
              </div>
              <div className="grid grid-cols-1 gap-3">
                {[
                  { id: 'rare', title: 'Focalisation Restreinte', desc: 'Moins de trois segments de trajet par cycle hebdomadaire.' },
                  { id: 'modere', title: 'Transit Urbain Linéaire', desc: 'Entre quatre et dix micro-trajets hebdomadaires.' },
                  { id: 'intensif', title: 'Déplacement Récurrent', desc: 'Plus de dix connexions par semaine, usage quotidien systématique.' },
                ].map(opt => (
                  <div 
                    key={opt.id}
                    onClick={() => updateField('motoTaxiUsage', opt.id)}
                    className={`p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 ${
                      formData.motoTaxiUsage === opt.id 
                        ? (darkMode ? 'border-emerald-500 bg-[#0e1726]' : 'border-emerald-600 bg-emerald-50/30') 
                        : (darkMode ? 'border-[#1e293b] bg-[#0d1321] hover:border-[#334155]' : 'border-[#e2e8f0] bg-white hover:border-[#cbd5e1]')
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-sm font-semibold tracking-tight">{opt.title}</h4>
                        <p className={`text-xs mt-1 leading-relaxed ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>{opt.desc}</p>
                      </div>
                      <div className={`w-3.5 h-3.5 rounded-full border flex items-center justify-center transition-all mt-0.5 ${
                        formData.motoTaxiUsage === opt.id ? 'border-emerald-500 bg-emerald-500' : 'border-[#475569]'
                      }`}>
                        {formData.motoTaxiUsage === opt.id && <div className="w-1.5 h-1.5 rounded-full bg-white"></div>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* STEP 3: INFRASTRUCTURE CLIMATIQUE & ENEO */}
          {step === 3 && (
            <div className="space-y-6 animate-[fadeIn_0.4s_ease-out]">
              <div>
                <h2 className="text-2xl font-bold tracking-tight mb-2">Vecteurs Énergétiques Domestiques</h2>
                <p className={`text-xs ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>Analyse de la charge induite par le refroidissement thermique et la consommation brute.</p>
              </div>
              <div className="space-y-5">
                <div>
                  <label className={`text-[11px] font-bold uppercase tracking-widest block mb-3 ${darkMode ? 'text-[#475569]' : 'text-[#94a3b8]'}`}>Système de Climatisation Actif</label>
                  <div className="grid grid-cols-2 gap-3">
                    {[
                      { id: 'oui', title: 'Actif' },
                      { id: 'non', title: 'Inexistant' }
                    ].map(opt => (
                      <button
                        key={opt.id}
                        type="button"
                        onClick={() => updateField('climatisation', opt.id)}
                        className={`p-3.5 rounded-xl border text-xs font-bold uppercase tracking-wider transition-all duration-200 ${
                          formData.climatisation === opt.id
                            ? 'bg-emerald-600 border-emerald-600 text-white'
                            : (darkMode ? 'bg-[#0d1321] border-[#1e293b] text-[#64748b] hover:border-[#334155]' : 'bg-white border-[#e2e8f0] text-[#475569] hover:border-[#cbd5e1]')
                        }`}
                      >
                        {opt.title}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className={`text-[11px] font-bold uppercase tracking-widest block mb-3 ${darkMode ? 'text-[#475569]' : 'text-[#94a3b8]'}`}>Seuils de facturation mensuelle Eneo / Générateur</label>
                  <select 
                    value={formData.factureElectricite} 
                    onChange={e => updateField('factureElectricite', e.target.value)}
                    className={`w-full text-xs font-medium tracking-wide rounded-xl p-4 border outline-none appearance-none transition-all duration-200 ${
                      darkMode ? 'bg-[#0d1321] border-[#1e293b] text-white focus:border-emerald-500' : 'bg-white border-[#e2e8f0] text-[#0f172a] focus:border-emerald-600'
                    }`}
                  >
                    <option value="">Sélectionner l'amplitude financière</option>
                    <option value="low">Inférieur à 15 000 XAF</option>
                    <option value="medium">De 15 000 XAF à 50 000 XAF</option>
                    <option value="high">Supérieur à 50 000 XAF</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* STEP 4: ALIMENTATION */}
          {step === 4 && (
            <div className="space-y-6 animate-[fadeIn_0.4s_ease-out]">
              <div>
                <h2 className="text-2xl font-bold tracking-tight mb-2">Bilan des Intrants Alimentaires</h2>
                <p className={`text-xs ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>Ratio d'impact lié à la chaîne d'importation logistique de vos denrées.</p>
              </div>
              <div className="grid grid-cols-1 gap-3">
                {[
                  { id: 'local-heavy', title: 'Circuits Courts Locaux', desc: 'Produits vivriers agricoles issus du secteur agricole de proximité.' },
                  { id: 'mixed', title: 'Régime Hybride Distribué', desc: 'Équilibre entre cultures maraîchères locales et protéines animales.' },
                  { id: 'import-heavy', title: 'Forte Dépendance Import', desc: 'Prédominance de produits manufacturés importés soumis au fret international.' },
                ].map(opt => (
                  <div 
                    key={opt.id}
                    onClick={() => updateField('alimentationType', opt.id)}
                    className={`p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 ${
                      formData.alimentationType === opt.id 
                        ? (darkMode ? 'border-emerald-500 bg-[#0e1726]' : 'border-emerald-600 bg-emerald-50/30') 
                        : (darkMode ? 'border-[#1e293b] bg-[#0d1321] hover:border-[#334155]' : 'border-[#e2e8f0] bg-white hover:border-[#cbd5e1]')
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-sm font-semibold tracking-tight">{opt.title}</h4>
                        <p className={`text-xs mt-1 leading-relaxed ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>{opt.desc}</p>
                      </div>
                      <div className={`w-3.5 h-3.5 rounded-full border flex items-center justify-center transition-all mt-0.5 ${
                        formData.alimentationType === opt.id ? 'border-emerald-500 bg-emerald-500' : 'border-[#475569]'
                      }`}>
                        {formData.alimentationType === opt.id && <div className="w-1.5 h-1.5 rounded-full bg-white"></div>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* STEP 5: TRAITEMENT RESIDUEL */}
          {step === 5 && (
            <div className="space-y-6 animate-[fadeIn_0.4s_ease-out]">
              <div>
                <h2 className="text-2xl font-bold tracking-tight mb-2">Cycle Exogène des Résidus</h2>
                <p className={`text-xs ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>Protocole appliqué pour l'élimination finale de vos déchets ménagers.</p>
              </div>
              <div className="grid grid-cols-1 gap-3">
                {[
                  { id: 'tri', title: 'Valorisation Organique', desc: 'Tri à la source, compostage domestique ou filières spécialisées.' },
                  { id: 'bac', title: 'Collecte Publique Centralisée', desc: 'Évacuation standard via les infrastructures de traitement de zone.' },
                  { id: 'incineration', title: 'Incinération Thermique Thermoplastique', desc: 'Combustion privée ou rejet hors structures régulées.' },
                ].map(opt => (
                  <div 
                    key={opt.id}
                    onClick={() => updateField('dechetsGestion', opt.id)}
                    className={`p-4 rounded-xl border text-left cursor-pointer transition-all duration-300 ${
                      formData.dechetsGestion === opt.id 
                        ? (darkMode ? 'border-emerald-500 bg-[#0e1726]' : 'border-emerald-600 bg-emerald-50/30') 
                        : (darkMode ? 'border-[#1e293b] bg-[#0d1321] hover:border-[#334155]' : 'border-[#e2e8f0] bg-white hover:border-[#cbd5e1]')
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-sm font-semibold tracking-tight">{opt.title}</h4>
                        <p className={`text-xs mt-1 leading-relaxed ${darkMode ? 'text-[#64748b]' : 'text-[#64748b]'}`}>{opt.desc}</p>
                      </div>
                      <div className={`w-3.5 h-3.5 rounded-full border flex items-center justify-center transition-all mt-0.5 ${
                        formData.dechetsGestion === opt.id ? 'border-emerald-500 bg-emerald-500' : 'border-[#475569]'
                      }`}>
                        {formData.dechetsGestion === opt.id && <div className="w-1.5 h-1.5 rounded-full bg-white"></div>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* DOCK INTERACTION SYSTEM */}
          <div className={`flex justify-between items-center pt-6 border-t mt-10 transition-colors duration-300 ${
            darkMode ? 'border-[#1e293b]' : 'border-[#e2e8f0]'
          }`}>
            <button
              type="button"
              onClick={handlePrev}
              disabled={step === 1}
              className={`text-xs font-bold uppercase tracking-wider px-5 py-3 rounded-lg transition-all ${
                step === 1 
                  ? 'opacity-20 cursor-not-allowed' 
                  : (darkMode ? 'bg-[#131c2e] text-[#94a3b8] hover:bg-[#1e293b] hover:text-white' : 'bg-[#f1f5f9] text-[#475569] hover:bg-[#e2e8f0]')
              }`}
            >
              Back
            </button>

            {step < 5 ? (
              <button
                type="button"
                onClick={handleNext}
                className="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold uppercase tracking-wider px-6 py-3 rounded-lg transition-all shadow-lg shadow-emerald-600/10 active:scale-[0.98]"
              >
                Next Sequence
              </button>
            ) : (
              <button
                type="submit"
                className={`text-white text-xs font-bold uppercase tracking-wider px-6 py-3 rounded-lg transition-all active:scale-[0.98] ${
                  darkMode ? 'bg-emerald-600 hover:bg-emerald-500' : 'bg-[#0f172a] hover:bg-[#1e293b]'
                }`}
              >
                Execute Analysis
              </button>
            )}
          </div>

        </form>
      </main>

      {/* MINIMAL FOOTER FOR BALANCING SYSTEM */}
      <footer className={`border-t text-[10px] font-mono font-medium text-center py-4 tracking-widest ${
        darkMode ? 'border-[#1e293b] text-[#334155]' : 'border-[#e2e8f0] text-[#94a3b8]'
      }`}>
        SECURE COMPLIANCE LAYER // DATA-ENCRYPTED-LOCAL
      </footer>

    </div>
  )
}