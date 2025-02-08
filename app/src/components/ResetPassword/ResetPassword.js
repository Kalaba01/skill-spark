import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { showToast } from "../ToastNotification/ToastNotification";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./ResetPassword.scss";

function ResetPassword() {
  const { uidb64, token } = useParams();
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    password: "",
    confirmPassword: ""
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.password || !formData.confirmPassword) {
      showToast(t("resetPassword.errors.missingFields"), "error");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      showToast(t("resetPassword.errors.passwordMismatch"), "error");
      return;
    }

    setLoading(true);

    try {
      await axios.post(`http://127.0.0.1:8000/api/password-reset/confirm/${uidb64}/${token}/`, {
        password: formData.password
      });

      showToast(t("resetPassword.successMessage"), "success");
      navigate("/");
    } catch (err) {
      showToast(err.response?.data?.error || t("resetPassword.errors.invalidToken"), "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="reset-password-container">
      <div className="reset-password-box">
        <h2>{t("resetPassword.title")}</h2>

        <form onSubmit={handleSubmit}>
          <label>{t("resetPassword.newPassword")}</label>
          <input
            type="password"
            name="password"
            placeholder={t("resetPassword.newPasswordPlaceholder")}
            value={formData.password}
            onChange={handleChange}
            required
          />

          <label>{t("resetPassword.confirmPassword")}</label>
          <input
            type="password"
            name="confirmPassword"
            placeholder={t("resetPassword.confirmPasswordPlaceholder")}
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? t("resetPassword.loading") : t("resetPassword.submitButton")}
          </button>
        </form>
      </div>
    </div>
  );
}

export default ResetPassword;
