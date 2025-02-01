import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import enTranslation from "./locales/en/global.json";
import bsTranslation from "./locales/bs/global.json";

const resources = {
    en: { translation: enTranslation },
    bs: { translation: bsTranslation },
  };

i18n.use(initReactI18next).init({
  resources,
  lng: localStorage.getItem("language") || "en",
  fallbackLng: "en",
  interpolation: {
    escapeValue: false
  }
});

export default i18n;
