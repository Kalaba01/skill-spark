import React from 'react';
import { useTranslation } from "react-i18next";
import './Footer.scss';

function Footer() {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div>© {currentYear} SkillSpark. {t("footer.rights")}</div>
    </footer>
  );
}

export default Footer;
