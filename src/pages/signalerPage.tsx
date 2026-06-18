import { LanguageProvider } from '../../App (copie)/context/LanguageContext'
import { ThemeProvider } from '../../App (copie)/context/ThemeContext'
import SignalerDepot from '../../App (copie)/pages/SignalerDepot'

export default function SignalerPage() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <SignalerDepot />
      </LanguageProvider>
    </ThemeProvider>
  )
}
