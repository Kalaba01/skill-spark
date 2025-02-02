import React, { useState } from "react";
import "./LandingPage.scss";
import { FaChevronDown } from "react-icons/fa";
import { Login, Register, TopBar } from "../index";
import { useTranslation } from "react-i18next";

function LandingPage() {
  const [faqOpen, setFaqOpen] = useState(null);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isRegisterOpen, setIsRegisterOpen] = useState(false);

  const { t } = useTranslation();

  const toggleFaq = (index) => {
    setFaqOpen(faqOpen === index ? null : index);
  };

  const openLogin = () => {
    setIsRegisterOpen(false);
    setIsLoginOpen(true);
  };

  const openRegister = () => {
    setIsLoginOpen(false);
    setIsRegisterOpen(true);
  };

  return (
    <div className="landing-page">
      {/* Top Bar */}
      <TopBar openLogin={openLogin} />

      {/* Hero Section */}
      <section className="hero">
        <h1>{t("landingPage.title")}</h1>
      </section>

      {/* Features Section */}
      <section id="features" className="features">
        <h2>{t("landingPage.whyChoose")}</h2>

        <div className="feature-item">
          <img src="https://placehold.co/600x400" alt="Feature 1" />
          <div>
            <h3>{t("landingPage.feature1Title")}</h3>
            <p>{t("landingPage.feature1Description")}</p>
          </div>
        </div>

        <div className="feature-item reverse">
          <img src="https://placehold.co/600x400" alt="Feature 2" />
          <div>
            <h3>{t("landingPage.feature2Title")}</h3>
            <p>{t("landingPage.feature2Description")}</p>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="faq">
        <h2>{t("landingPage.faqTitle")}</h2>
        {t("landingPage.faqItems", { returnObjects: true }).map((faq, index) => (
          <div
            key={index}
            className={`faq-item ${faqOpen === index ? "open" : ""}`}
            onClick={() => toggleFaq(index)}
          >
            <div className="faq-header">
              <h3>{faq.question}</h3>
              <FaChevronDown className={`arrow ${faqOpen === index ? "rotate" : ""}`} />
            </div>
            <div className="faq-answer">
              {faqOpen === index && <p>{faq.answer}</p>}
            </div>
          </div>
        ))}
      </section>

      {/* Login and Register Popups */}
      <Login isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} switchToRegister={openRegister} />
      <Register isOpen={isRegisterOpen} onClose={() => setIsRegisterOpen(false)} switchToLogin={openLogin} />

    </div>
  );
}

export default LandingPage;
