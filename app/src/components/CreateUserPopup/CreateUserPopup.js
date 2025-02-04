import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import axios from "axios";
import { showToast } from "../ToastNotification/ToastNotification";
import "./CreateUserPopup.scss";

const CreateUserPopup = ({ user, onClose, refresh, companies }) => {
  const { t } = useTranslation();
  const isEditing = Boolean(user);

  const [formData, setFormData] = useState({
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    email: user?.email || "",
    password: "",
    role: user?.role || "",
    company_name: user?.company_name || (isEditing && user?.role === "employee" ? user.company_name : "")
  });

  const [roleSelected, setRoleSelected] = useState(isEditing);

  useEffect(() => {
    if (isEditing) {
      setFormData({
        first_name: user.first_name || "",
        last_name: user.last_name || "",
        email: user.email || "",
        password: "",
        role: user.role || "",
        company_name: user.role === "employee" ? user.working_at || "" : ""
      });
    }
  }, [isEditing, user]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });

    if (e.target.name === "role" && !isEditing) {
      setRoleSelected(true);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");

    try {
      if (isEditing) {
        await axios.put(`http://127.0.0.1:8000/api/user-management/users/${user.id}/`, formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
        showToast(t("userManagement.editSuccess"), "success");
      } else {
        await axios.post("http://127.0.0.1:8000/api/user-management/users/", formData, {
          headers: { Authorization: `Bearer ${token}` },
        });
        showToast(t("userManagement.addSuccess"), "success");
      }
      refresh();
      onClose();
    } catch (error) {
      console.error("Error saving user:", error);
      showToast(t("userManagement.error"), "error");
    }
  };

  return (
    <div className="popup-overlay" onClick={onClose}>
      <div className="popup-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>&times;</button>
        <h2>{isEditing ? t("userManagement.editUser") : t("userManagement.addUser")}</h2>

        <form onSubmit={handleSubmit}>
          {!isEditing && (
            <select name="role" value={formData.role} onChange={handleChange} required>
              <option value="">{t("userManagement.choseRole")}</option>
              <option value="admin">{t("userManagement.admin")}</option>
              <option value="company">{t("userManagement.company")}</option>
              <option value="employee">{t("userManagement.employee")}</option>
            </select>
          )}

          {roleSelected && (
            <>
              <input
                type="text"
                name="first_name"
                placeholder={t("userManagement.firstName")}
                value={formData.first_name}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="last_name"
                placeholder={t("userManagement.lastName")}
                value={formData.last_name}
                onChange={handleChange}
                required
              />
              <input
                type="email"
                name="email"
                placeholder={t("userManagement.email")}
                value={formData.email}
                onChange={handleChange}
                required
              />
              {!isEditing && (
                <input
                  type="password"
                  name="password"
                  placeholder={t("userManagement.password")}
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              )}

              {formData.role === "company" && (
                <input
                  type="text"
                  name="company_name"
                  placeholder={t("userManagement.companyName")}
                  value={formData.company_name}
                  onChange={handleChange}
                  required
                />
              )}

              {formData.role === "employee" && (
                <select
                    name="company_name"
                    value={formData.company_name}
                    onChange={handleChange}
                    required
                >
                    <option value="">{t("userManagement.selectCompany")}</option>
                    {companies.map((company, index) => (
                    <option key={index} value={company}>
                        {company}
                    </option>
                    ))}
                </select>
                )}


              <button type="submit">{t("userManagement.save")}</button>
            </>
          )}
        </form>
      </div>
    </div>
  );
};

export default CreateUserPopup;
