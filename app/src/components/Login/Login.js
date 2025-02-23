import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { showToast } from "../ToastNotification/ToastNotification";
import { useTranslation } from "react-i18next";
import { jwtDecode } from "jwt-decode";
import axios from "axios";
import "./Login.scss";

/**
 * Login Component
 *
 * - Displays a login form for user authentication.
 * - Uses Axios to send login credentials to the backend.
 * - Stores JWT tokens in local storage upon successful login.
 * - Decodes JWT to determine the user's role and redirects accordingly.
 * - Supports switching to registration and password reset views.
 */

function Login({ isOpen, onClose, switchToRegister, switchToForgotPassword }) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });

  // Updates form data when the user types into input fields
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Handles form submission, sends login request, and processes response
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      showToast(t("login.errors.missingFields"), "error");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/auth/login/", {
        email: formData.email,
        password: formData.password
      });

      showToast(t("login.success"), "success");

      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);

      const decodedToken = jwtDecode(response.data.access);
      const userRole = decodedToken.user.role;

      if (userRole === "admin") {
        navigate("/admin");
      } else if (userRole === "company") {
        navigate("/company");
      } else if (userRole === "employee") {
        navigate("/employee");
      } else {
        navigate("/");
      }
    } catch (err) {
      showToast(err.response?.data?.message || t("login.errors.invalidCredentials"), "error");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="login-overlay" onClick={onClose}>
      <div className="login-popup" onClick={(e) => e.stopPropagation()}>
        <h2>{t("login.title")}</h2>

        <form onSubmit={handleSubmit}>
          <label>{t("login.email")}</label>
          <input
            type="email"
            name="email"
            placeholder={t("login.emailPlaceholder")}
            required
            value={formData.email}
            onChange={handleChange}
          />

          <label>{t("login.password")}</label>
          <input
            type="password"
            name="password"
            placeholder={t("login.passwordPlaceholder")}
            required
            value={formData.password}
            onChange={handleChange}
          />

          <p className="forgot-password" onClick={switchToForgotPassword}>{t("login.forgotPassword")}</p>

          <button type="submit" className="login-btn">{t("login.button")}</button>
        </form>

        <p className="register-link">
          {t("login.noAccount")} <span onClick={switchToRegister}>{t("login.register")}</span>
        </p>

        <button className="close-btn" onClick={onClose}>&times;</button>
      </div>
    </div>
  );
}

export default Login;
