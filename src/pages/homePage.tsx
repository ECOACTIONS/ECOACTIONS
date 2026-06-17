import { Link } from 'react-router-dom'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans antialiased text-slate-800 flex flex-col">
      
      {/* 1. NAVBAR PREMIUM (Responsive & Glassmorphism) */}
      <nav className="sticky top-0 z-50 bg-white/70 backdrop-blur-md border-b border-slate-100 px-4 sm:px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 bg-emerald-600 rounded-xl flex items-center justify-center shadow-md shadow-emerald-600/10">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.5A7 7 0 0111 20z" />
              </svg>
            </div>
            <span className="text-lg font-bold text-slate-900 tracking-tight">EcoImpact AI</span>
          </div>
          
          {/* Liens - Cachés sur petits mobiles, visibles sur tablettes/PC */}
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
            <a href="#solutions" className="hover:text-emerald-600 transition-colors">Solutions</a>
            <a href="#impact" className="hover:text-emerald-600 transition-colors">Notre Impact</a>
            <a href="#partenaires" className="hover:text-emerald-600 transition-colors">Communauté</a>
           
          </div>
          
          {/* Actions */}
          <div className="flex items-center gap-3 sm:gap-4">
            <Link to="/login" className="text-sm font-semibold text-slate-600 hover:text-slate-900 transition-colors px-2 py-1">
              Se connecter
            </Link>
            <Link to="/register" className="bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium px-4 py-2.5 rounded-xl transition-all shadow-sm active:scale-[0.98]">
              S'inscrire
            </Link>
            
          </div>
        </div>
      </nav>

      {/* 2. HERO SECTION (Optimisé mobile) */}
      <section id="solutions" className="max-w-4xl mx-auto text-center px-4 sm:px-6 pt-16 md:pt-24 pb-16 flex-1">
        {/* Badge Contextuel */}
        <div className="inline-flex items-center gap-2 bg-emerald-50 border border-emerald-100 rounded-full px-4 py-1.5 mb-6 active:scale-95 transition-transform cursor-pointer">
          <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-[11px] font-bold text-emerald-800 tracking-wide uppercase">Tech Verte • Cameroun</span>
        </div>

        {/* Titre Majeur */}
        <h1 className="text-3xl sm:text-4xl md:text-6xl font-black text-slate-900 tracking-tight leading-[1.15] mb-6 px-2">
          Réduisez votre empreinte <br className="hidden sm:inline" />
          <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">à votre rythme</span>
        </h1>

        {/* Description */}
        <p className="text-sm sm:text-base md:text-lg text-slate-500 max-w-2xl mx-auto leading-relaxed mb-10 px-4">
          EcoImpact AI analyse vos habitudes environnementales et génère un plan d'action sur-mesure, calibré pour les réalités camerounaises (<span className="font-semibold text-slate-700">motos, générateurs, gestion locale des déchets</span>).
        </p>

        {/* Boutons d'actions adaptatifs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 max-w-md mx-auto sm:max-w-none px-4">
          <Link 
            to="/register" 
            className="w-full sm:w-auto bg-slate-900 hover:bg-slate-800 text-white font-semibold px-8 py-3.5 rounded-xl transition-all duration-200 shadow-lg shadow-slate-900/10 active:scale-[0.99] text-center text-sm"
          >
            Calculer mon empreinte
          </Link>
          <a 
            href="#impact" 
            className="w-full sm:w-auto border border-slate-200 bg-white hover:bg-slate-50 text-slate-600 font-medium px-8 py-3.5 rounded-xl transition-all text-center text-sm"
          >
            Découvrir l'impact
          </a>
        </div>
      </section>

      {/* 3. SECTION STATISTIQUES / BENTO GRID */}
      <section id="impact" className="max-w-5xl mx-auto px-4 sm:px-6 py-12 w-full">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Carte 1 */}
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-emerald-500/20 transition-all duration-300 group">
            <div className="w-10 h-10 bg-emerald-50 group-hover:bg-emerald-100 rounded-xl flex items-center justify-center mb-5 transition-colors">
              <svg className="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
              </svg>
            </div>
            <div className="text-3xl font-black text-slate-900 tracking-tight mb-1">-30%</div>
            <div className="text-sm font-bold text-slate-800 mb-1">Réduction moyenne</div>
            <p className="text-xs text-slate-400 leading-relaxed">Baisse des émissions de CO₂ constatée dès le premier trimestre d'utilisation.</p>
          </div>

          {/* Carte 2 */}
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-emerald-500/20 transition-all duration-300 group">
            <div className="w-10 h-10 bg-emerald-50 group-hover:bg-emerald-100 rounded-xl flex items-center justify-center mb-5 transition-colors">
              <svg className="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="text-3xl font-black text-slate-900 tracking-tight mb-1">15 000 XAF</div>
            <div className="text-sm font-bold text-slate-800 mb-1">Économisés par mois</div>
            <p className="text-xs text-slate-400 leading-relaxed">Économies directes générées sur les factures d'énergie et de carburant.</p>
          </div>

          {/* Carte 3 */}
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-emerald-500/20 transition-all duration-300 group">
            <div className="w-10 h-10 bg-emerald-50 group-hover:bg-emerald-100 rounded-xl flex items-center justify-center mb-5 transition-colors">
              <svg className="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            </div>
            <div className="text-3xl font-black text-slate-900 tracking-tight mb-1">100%</div>
            <div className="text-sm font-bold text-slate-800 mb-1">Contexte Localisé</div>
            <p className="text-xs text-slate-400 leading-relaxed">Algorithmes entraînés selon les infrastructures et données énergétiques du pays.</p>
          </div>

        </div>
      </section>

      {/* 4. BANNIÈRE FINALE D'ENGAGEMENT */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 pt-12 pb-20 w-full">
        <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-2xl p-8 md:p-12 text-center shadow-xl relative overflow-hidden">
          <div className="absolute inset-0 opacity-5 bg-[radial-gradient(#10b981_1px,transparent_1px)] [background-size:16px_16px]"></div>
          
          <div className="relative z-10 max-w-lg mx-auto">
            <h2 className="text-2xl md:text-3xl font-bold text-white tracking-tight mb-3">
              Prêt à agir pour votre planète ?
            </h2>
            <p className="text-xs md:text-sm text-slate-400 mb-8 leading-relaxed">
              Rejoignez les citoyens et entreprises au Cameroun qui optimisent leur empreinte écologique avec l'IA.
            </p>
            <Link 
              to="/register" 
              className="inline-block bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold px-8 py-3.5 rounded-xl transition-all shadow-md shadow-emerald-600/10 active:scale-[0.99]"
            >
              Créer mon compte gratuitement
            </Link>
          </div>
        </div>
      </section>

      {/* 5. FOOTER PROFESSIONNEL ET INSTITUTIONNEL */}
      <footer className="bg-white border-t border-slate-100 mt-auto">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12">
          
          {/* Structure Grille Principale */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
            
            {/* Colonne Marque / Bio */}
            <div className="col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-7 h-7 bg-emerald-600 rounded-lg flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 20A7 7 0 019.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.5 1 9.5A7 7 0 0111 20z" />
                  </svg>
                </div>
                <span className="text-sm font-bold text-slate-900 tracking-tight">EcoImpact AI</span>
              </div>
              <p className="text-xs text-slate-400 max-w-sm leading-relaxed mb-4">
                Première plateforme d'intelligence artificielle dédiée à la comptabilité carbone et à la transition écologique au Cameroun.
              </p>
              <div className="text-[11px] text-slate-400 font-medium">
                📍 Douala • Yaoundé, Cameroun
              </div>
            </div>

            {/* Liens Produit */}
            <div>
              <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-4">Application</h4>
              <ul className="space-y-2.5 text-xs font-medium text-slate-500">
                <li><a href="#solutions" className="hover:text-emerald-600 transition-colors">Calculateur</a></li>
                <li><a href="#impact" className="hover:text-emerald-600 transition-colors">Simulateur XAF</a></li>
                <li><Link to="/login" className="hover:text-emerald-600 transition-colors">Tableau de bord</Link></li>
              </ul>
            </div>

            {/* Liens Ressources */}
            <div>
              <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-4">Ressources</h4>
              <ul className="space-y-2.5 text-xs font-medium text-slate-500">
                <li><a href="#" className="hover:text-emerald-600 transition-colors">Données Climat</a></li>
                <li><a href="#" className="hover:text-emerald-600 transition-colors">Guide Éco-Geste</a></li>
                <li><a href="#" className="hover:text-emerald-600 transition-colors">Support Tech</a></li>
              </ul>
            </div>

            {/* Liens Légal */}
            <div>
              <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-4">Juridique</h4>
              <ul className="space-y-2.5 text-xs font-medium text-slate-500">
                <li><a href="#" className="hover:text-emerald-600 transition-colors">Confidentialité</a></li>
                <li><a href="#" className="hover:text-emerald-600 transition-colors">Conditions d'usage</a></li>
                <li><a href="#" className="hover:text-emerald-600 transition-colors">Mentions Légales</a></li>
              </ul>
            </div>

          </div>

          {/* Barre de copyright finale */}
          <div className="border-t border-slate-100 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] font-medium text-slate-400">
            <div>
              &copy; {new Date().getFullYear()} EcoImpact AI. Tous droits réservés.
            </div>
            <div className="flex gap-6">
              <a href="#" className="hover:text-slate-600 transition-colors">Twitter (X)</a>
              <a href="#" className="hover:text-slate-600 transition-colors">LinkedIn</a>
              <a href="#" className="hover:text-slate-600 transition-colors">GitHub</a>
            </div>
          </div>

        </div>
      </footer>

    </div>
  )
}