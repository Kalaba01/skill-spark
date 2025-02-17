import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { showToast } from "../ToastNotification/ToastNotification";
import { FaTimes } from "react-icons/fa";
import axios from "axios";
import "./EmployeeProfileEdit.scss";

const EmployeeProfileEdit = ({ profile, onClose, refreshProfile }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    first_name: profile.first_name,
    last_name: profile.last_name,
    email: profile.email,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("access_token");
      await axios.post("http://127.0.0.1:8000/api/user-management/profile/", formData, {
        headers: { Authorization: `Bearer ${token}` },
      });

      refreshProfile();
      onClose();
      showToast(t("employeeProfileEdit.successMessage"), "success");
    } catch (error) {
      console.error("Error updating profile:", error);
      setError(t("employeeProfileEdit.updateError"));
      showToast(t("employeeProfileEdit.updateError"), "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="edit-profile-modal">
      <div className="modal-content">
        <button className="close-btn" onClick={onClose}>
          <FaTimes />
        </button>
        <h2>{t("employeeProfileEdit.title")}</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>{t("employeeProfile.firstName")}</label>
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="input-group">
            <label>{t("employeeProfile.lastName")}</label>
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="input-group">
            <label>{t("employeeProfile.email")}</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <button className="save-btn" type="submit" disabled={loading}>
            {loading ? t("employeeProfileEdit.saving") : t("employeeProfileEdit.saveChanges")}
          </button>
        </form>
      </div>
    </div>
  );
};

export default EmployeeProfileEdit;
