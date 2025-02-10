import React, { useState } from "react";
import { Login, Register, ForgotPassword, TopBar } from "../index";
import { useTranslation } from "react-i18next";
import { FaChevronDown } from "react-icons/fa";
import { ReactTyped } from "react-typed";
import "./LandingPage.scss";

function LandingPage() {
  const [faqOpen, setFaqOpen] = useState(null);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isRegisterOpen, setIsRegisterOpen] = useState(false);
  const [isForgotPasswordOpen, setIsForgotPasswordOpen] = useState(false);

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

  const openForgotPassword = () => {
    setIsLoginOpen(false);
    setIsRegisterOpen(false);
    setIsForgotPasswordOpen(true);
  };

  return (
    <div className="landing-page">
      {/* Top Bar */}
      <TopBar openLogin={openLogin} />

      {/* Hero Section */}
      <section className="hero">
      <h1>
          <ReactTyped
            strings={[t("landingPage.title")]}
            typeSpeed={50}
            loop={false}
            showCursor={true}
          />
        </h1>
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

      {/* Login, Register and Forgot Password popups */}
      <Login isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} switchToRegister={openRegister} switchToForgotPassword={openForgotPassword} />
      <Register isOpen={isRegisterOpen} onClose={() => setIsRegisterOpen(false)} switchToLogin={openLogin} />
      <ForgotPassword isOpen={isForgotPasswordOpen} onClose={() => setIsForgotPasswordOpen(false)} />
    </div>
  );
}

export default LandingPage;
