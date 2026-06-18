import { useState, useRef, useEffect } from 'react'

interface Message {
  id: string
  sender: 'user' | 'ai'
  text: string
  timestamp: string
}

interface ChatbotProps {
  // Le chatbot reçoit le formData du calculateur en prop pour connaître le contexte de l'utilisateur
  userContext: {
    transportType: string
    motoTaxiUsage: string
    climatisation: string
    factureElectricite: string
    alimentationType: string
    dechetsGestion: string
  }
}

export default function ChatbotSection({ userContext }: ChatbotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init',
      sender: 'ai',
      text: "Bonjour ! J'ai analysé votre bilan carbone au Cameroun. Je connais vos habitudes de consommation. Comment puis-je vous aider à optimiser votre plan d'action aujourd'hui ?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ])
  const [input, setInput] = useState<string>('')
  const [isTyping, setIsTyping] = useState<boolean>(false)
  const chatEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll vers le dernier message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Math.random().toString(),
      sender: 'user',
      text: input,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    setMessages(prev => [...prev, userMessage])
    const currentInput = input
    setInput('')
    setIsTyping(true)

    try {
      // Connexion chirurgicale avec le backend
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: currentInput,
          // ON ENVOIE LE CONTEXTE DU FORMULAIRE AU BACKEND ICI 
          context: userContext,
          // Optionnel : envoyer l'historique si le backend gère la mémoire
          history: messages.map(m => ({ role: m.sender === 'user' ? 'user' : 'assistant', content: m.text }))
        })
      })

      if (!response.ok) throw new Error()
      const data = await response.json()

      setMessages(prev => [...prev, {
        id: Math.random().toString(),
        sender: 'ai',
        text: data.reply || "Désolé, mon module d'analyse a rencontré une anomalie.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }])
    } catch (error) {
      // Simulation offline en cas de coupure ou si le backend n'est pas encore prêt
      setTimeout(() => {
        setMessages(prev => [...prev, {
          id: Math.random().toString(),
          sender: 'ai',
          text: `[Mode Démo] Vous me parlez de "${currentInput}". En production, mon modèle analysera cela en fonction de votre facteur d'impact (Facture Eneo: ${userContext.factureElectricite}, Transport: ${userContext.transportType}).`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }])
      }, 1000)
    } finally {
      setIsTyping(false)
    }
  }

  return (
    <div className="w-full border border-[#1e293b] rounded-2xl bg-[#0d1321] overflow-hidden flex flex-col h-[450px] shadow-2xl shadow-black/40">
      
      {/* CHAT HEADER */}
      <div className="bg-[#0b0f19] border-b border-[#1e293b] px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-[#94a3b8]">
            Assistant Climatique Virtuel
          </span>
        </div>
        <span className="text-[9px] font-mono bg-[#162235] text-emerald-400 px-2 py-0.5 rounded font-bold">
          CONTEXTE SYNCHRONISÉ
        </span>
      </div>

      {/* MESSAGES CONTAINER */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-slate-800">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
            <div className={`max-w-[85%] rounded-xl px-3.5 py-2.5 text-xs leading-relaxed ${
              msg.sender === 'user' 
                ? 'bg-emerald-600 text-white rounded-tr-none' 
                : 'bg-[#131c2e] text-[#f8fafc] rounded-tl-none border border-[#1e293b]'
            }`}>
              {msg.text}
            </div>
            <span className="text-[8px] font-mono text-[#475569] mt-1 px-1">{msg.timestamp}</span>
          </div>
        ))}

        {/* LOADING INDICATOR */}
        {isTyping && (
          <div className="flex flex-col items-start">
            <div className="bg-[#131c2e] border border-[#1e293b] text-[#64748b] rounded-xl rounded-tl-none px-4 py-2.5 text-xs font-mono tracking-widest animate-pulse">
              AI ANALYZING DATA...
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* INPUT BAR */}
      <form onSubmit={handleSendMessage} className="p-3 bg-[#0b0f19] border-t border-[#1e293b] flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Posez une question sur votre empreinte..."
          className="flex-1 bg-[#050911] border border-[#1e293b] rounded-xl px-3 text-xs text-white focus:outline-none focus:border-emerald-500 transition-colors placeholder-[#334155]"
        />
        <button
          type="submit"
          className="bg-emerald-600 hover:bg-emerald-500 font-mono text-[10px] text-white font-bold uppercase tracking-wider px-4 rounded-xl transition-colors"
        >
          SEND
        </button>
      </form>

    </div>
  )
}