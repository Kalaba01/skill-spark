import React, { useState } from "react";
import axios from "axios";
import { showToast } from "../ToastNotification/ToastNotification";
import "./Register.scss";
import { useTranslation } from "react-i18next";

function Register({ isOpen, onClose, switchToLogin }) {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    company_name: "",
    email: "",
    password: "",
    confirm_password: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirm_password) {
      showToast(t("register.errors.passwordMismatch"), "error");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/auth/register/", {
        company_name: formData.company_name,
        email: formData.email,
        password: formData.password
      });

      showToast(response.data.message, "success");

      setFormData({
        company_name: "",
        email: "",
        password: "",
        confirm_password: ""
      });

      setTimeout(() => {
        switchToLogin();
      }, 2000);
    } catch (err) {
      showToast(err.response?.data?.message || t("register.errors.failed"), "error");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="register-overlay" onClick={onClose}>
      <div className="register-popup" onClick={(e) => e.stopPropagation()}>
        <h2>{t("register.title")}</h2>

        <form onSubmit={handleSubmit}>
          <label>{t("register.companyName")}</label>
          <input
            type="text"
            name="company_name"
            placeholder={t("register.companyPlaceholder")}
            required
            value={formData.company_name}
            onChange={handleChange}
          />

          <label>{t("register.email")}</label>
          <input
            type="email"
            name="email"
            placeholder={t("register.emailPlaceholder")}
            required
            value={formData.email}
            onChange={handleChange}
          />

          <label>{t("register.password")}</label>
          <input
            type="password"
            name="password"
            placeholder={t("register.passwordPlaceholder")}
            required
            value={formData.password}
            onChange={handleChange}
          />

          <label>{t("register.confirmPassword")}</label>
          <input
            type="password"
            name="confirm_password"
            placeholder={t("register.confirmPasswordPlaceholder")}
            required
            value={formData.confirm_password}
            onChange={handleChange}
          />

          <button type="submit" className="register-btn">{t("register.button")}</button>
        </form>

        <p className="login-link">
          {t("register.alreadyHaveAccount")} <span onClick={switchToLogin}>{t("register.login")}</span>
        </p>

        <button className="close-btn" onClick={onClose}>&times;</button>
      </div>
    </div>
  );
}

export default Register;
