import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { showToast } from "../ToastNotification/ToastNotification";
import axios from "axios";
import "./CreateUserPopup.scss";

/**
 * CreateUserPopup component.
 * - Used for creating and editing users (Admin, Company, Employee).
 * - Handles form submission for user creation and updates.
 * - Provides validation and displays error/success messages.
 */

const CreateUserPopup = ({ user, onClose, refresh, companies }) => {
  const { t } = useTranslation();
  const isEditing = Boolean(user);

  const [formData, setFormData] = useState({
    email: user?.email || "",
    password: "",
    role: user?.role || "",
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    company_name: user?.company_name || (isEditing && user?.role === "employee" ? user.working_at : "")
  });

  const [roleSelected, setRoleSelected] = useState(isEditing);

  // Update form data if user is being edited
  useEffect(() => {
    if (isEditing) {
      setFormData({
        email: user.email || "",
        password: "",
        role: user.role || "",
        first_name: user.first_name || "",
        last_name: user.last_name || "",
        company_name: user.role === "employee" ? user.working_at || "" : user.company_name || ""
      });
    }
  }, [isEditing, user]);

  // Handles input field changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });

    if (e.target.name === "role" && !isEditing) {
      setRoleSelected(true);
    }
  };

  // Handles form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");

    let filteredData = { ...formData };

    if (formData.role !== "company" && formData.role !== "employee") {
        delete filteredData.company_name;
    }

    try {
        if (isEditing) {
            await axios.put(`http://127.0.0.1:8000/api/user-management/users/${user.id}/`, filteredData, {
                headers: { Authorization: `Bearer ${token}` },
            });
            showToast(t("userManagement.editSuccess"), "success");
        } else {
            await axios.post("http://127.0.0.1:8000/api/user-management/users/", filteredData, {
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
          {/* Role Selection (only when creating a new user) */}
          {!isEditing && (
            <select name="role" value={formData.role} onChange={handleChange} required>
              <option value="">{t("userManagement.choseRole")}</option>
              <option value="admin">{t("userManagement.admin")}</option>
              <option value="company">{t("userManagement.company")}</option>
              <option value="employee">{t("userManagement.employee")}</option>
            </select>
          )}

          {/* Admin Role Fields */}
          {roleSelected && formData.role === "admin" && (
            <>
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
            </>
          )}

          {/* Company Role Fields */}
          {roleSelected && formData.role === "company" && (
            <>
              <input
                type="text"
                name="company_name"
                placeholder={t("userManagement.companyName")}
                value={formData.company_name}
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
            </>
          )}

          {/* Employee Role Fields */}
          {roleSelected && formData.role === "employee" && (
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

              {/* Company selection for employees */}
              <select name="company_name" value={formData.company_name} onChange={handleChange} required>
                <option value="">{t("userManagement.selectCompany")}</option>
                {companies.map((company, index) => (
                  <option key={index} value={company}>
                    {company}
                  </option>
                ))}
              </select>
            </>
          )}

          <button type="submit">{t("userManagement.save")}</button>
        </form>
      </div>
    </div>
  );
};

export default CreateUserPopup;
