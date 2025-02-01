import React from 'react';
import './Footer.scss';
import { useTranslation } from "react-i18next";

function Footer() {
  const { t } = useTranslation();

  return (
    <footer className="footer">
      <div>© 2025 SkillSpark. {t("footer.rights")}</div>
    </footer>
  );
}

export default Footer;
