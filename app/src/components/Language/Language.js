import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setLanguage } from "../../store/languageSlice";
import { useTranslation } from "react-i18next";
import { FaGlobe, FaCheck } from "react-icons/fa";
import "./Language.scss";

/**
 * Language Component
 * - Provides a language selection dropdown for switching between English and Bosnian.
 * - Uses Redux to store the selected language globally.
 * - Updates the `i18next` instance to apply the language change.
 * - Displays a checkmark next to the currently selected language.
 */

function Language() {
  const { i18n } = useTranslation();
  const dispatch = useDispatch();
  const language = useSelector((state) => state.language.language);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  // Changes the language in the Redux store and updates i18next
  const changeLanguage = (lang) => {
    dispatch(setLanguage(lang));
    i18n.changeLanguage(lang);
    setDropdownOpen(false);
  };

  return (
    <div className="language-container">
      <div className="language-icon" onClick={() => setDropdownOpen(!dropdownOpen)}>
        <FaGlobe size={24} />
      </div>
      {dropdownOpen && (
        <div className="language-dropdown">
          <div className="language-option" onClick={() => changeLanguage("en")}>
            English {language === "en" && <FaCheck />}
          </div>
          <div className="language-option" onClick={() => changeLanguage("bs")}>
            Bosanski {language === "bs" && <FaCheck />}
          </div>
        </div>
      )}
    </div>
  );
}

export default Language;
