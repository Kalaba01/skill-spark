import React, { useState } from "react";
import { showToast } from "../ToastNotification/ToastNotification";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./ForgotPassword.scss";

/**
 * ForgotPassword Component
 *
 * - Displays a modal popup for users to request a password reset.
 * - Sends a password reset request to the backend when the form is submitted.
 * - Shows success or error messages using toast notifications.
 */

function ForgotPassword({ isOpen, onClose }) {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");

  // Handles the password reset form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) {
      showToast(t("forgotPassword.errors.missingEmail"), "error");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:8000/api/password-reset/", { email });
      showToast(t("forgotPassword.successMessage"), "success");
      setEmail("");
    } catch (err) {
      showToast(t("forgotPassword.errors.failedRequest"), "error");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="forgot-password-overlay" onClick={onClose}>
      <div className="forgot-password-popup" onClick={(e) => e.stopPropagation()}>
        <h2>{t("forgotPassword.title")}</h2>

        <form onSubmit={handleSubmit}>
          <label>{t("forgotPassword.email")}</label>
          <input
            type="email"
            placeholder={t("forgotPassword.emailPlaceholder")}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <button type="submit" className="submit-btn">{t("forgotPassword.submitButton")}</button>
        </form>

        <button className="close-btn" onClick={onClose}>&times;</button>
      </div>
    </div>
  );
}

export default ForgotPassword;
