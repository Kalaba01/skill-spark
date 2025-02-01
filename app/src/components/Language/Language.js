import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setLanguage } from "../../store/languageSlice";
import { useTranslation } from "react-i18next";
import { FaGlobe, FaCheck } from "react-icons/fa";
import "./Language.scss";

function Language() {
  const dispatch = useDispatch();
  const language = useSelector((state) => state.language.language);
  const { i18n } = useTranslation();
  const [dropdownOpen, setDropdownOpen] = useState(false);

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
