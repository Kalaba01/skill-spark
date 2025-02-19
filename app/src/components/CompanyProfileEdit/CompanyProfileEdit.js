import React, { useState } from "react";
import { FaTimes, FaSave } from "react-icons/fa";
import axios from "axios";
import { useTranslation } from "react-i18next";
import { showToast } from "../ToastNotification/ToastNotification";
import "./CompanyProfileEdit.scss";

const CompanyProfileEdit = ({ company, onClose, refreshProfile }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    company_name: company.company_name,
    email: company.email,
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      await axios.post(
        "http://127.0.0.1:8000/api/user-management/company-profile/",
        formData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      showToast(t("companyProfileEdit.successMessage"));
      refreshProfile();
      onClose();
    } catch (error) {
      console.error("Error updating profile:", error);
      showToast(t("companyProfileEdit.errorMessage"), "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="company-profile-edit-overlay">
      <div className="company-profile-edit">
        <div className="header">
          <h2>{t("companyProfileEdit.title")}</h2>
          <FaTimes className="close-icon" onClick={onClose} />
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>{t("companyProfileEdit.companyName")}</label>
            <input
              type="text"
              name="company_name"
              value={formData.company_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="input-group">
            <label>{t("companyProfileEdit.email")}</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="save-btn" disabled={loading}>
            <FaSave /> {loading ? t("companyProfileEdit.saving") : t("companyProfileEdit.save")}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CompanyProfileEdit;
