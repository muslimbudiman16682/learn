import i18n from "i18next"
import { initReactI18next } from "react-i18next"

import en from "./locales/en.json"
import id from "./locales/id.json"

export const LANGUAGE_STORAGE_KEY = "language"
export const DEFAULT_LANGUAGE = "id"
export const SUPPORTED_LANGUAGES = ["id", "en"] as const
export type SupportedLanguage = (typeof SUPPORTED_LANGUAGES)[number]

const getInitialLanguage = (): SupportedLanguage => {
  const stored = localStorage.getItem(LANGUAGE_STORAGE_KEY)
  if (stored && (SUPPORTED_LANGUAGES as readonly string[]).includes(stored)) {
    return stored as SupportedLanguage
  }
  return DEFAULT_LANGUAGE
}

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    id: { translation: id },
  },
  lng: getInitialLanguage(),
  fallbackLng: DEFAULT_LANGUAGE,
  interpolation: {
    escapeValue: false,
  },
})

export const changeLanguage = (language: SupportedLanguage) => {
  localStorage.setItem(LANGUAGE_STORAGE_KEY, language)
  i18n.changeLanguage(language)
}

export default i18n
