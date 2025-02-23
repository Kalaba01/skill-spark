import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { showToast } from "../ToastNotification/ToastNotification";
import axios from "axios";
import "./EmployeePopup.scss";

/**
 * EmployeePopup component.
 * - Handles adding and editing employees.
 * - Uses a form to collect employee details.
 * - Sends API requests to create or update employees.
 */

const EmployeePopup = ({ employee, onClose, refresh }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    first_name: employee?.first_name || "",
    last_name: employee?.last_name || "",
    email: employee?.email || "",
    password: ""
  });

  // Handles input changes and updates the form state
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handles form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");

    try {
      if (employee) {
        await axios.put(
          `http://127.0.0.1:8000/api/user-management/employees/${employee.id}/`,
          { first_name: formData.first_name, last_name: formData.last_name, email: formData.email },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        showToast(t("employeeManagement.editSuccess"), "success");
      } else {
        await axios.post(
          "http://127.0.0.1:8000/api/user-management/employees/",
          formData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        showToast(t("employeeManagement.addSuccess"), "success");
      }
      refresh();
      onClose();
    } catch (error) {
      console.error("Error saving employee:", error);
      showToast(t("employeeManagement.error"), "error");
    }
  };

  return (
    <div className="popup-overlay" onClick={onClose}>
      <div className="popup-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>&times;</button>

        <h2>{employee ? t("employeeManagement.editEmployee") : t("employeeManagement.addEmployee")}</h2>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="first_name"
            placeholder={t("employeeManagement.firstName")}
            value={formData.first_name}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="last_name"
            placeholder={t("employeeManagement.lastName")}
            value={formData.last_name}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder={t("employeeManagement.email")}
            value={formData.email}
            onChange={handleChange}
            required
          />
          {!employee && (
            <input
              type="password"
              name="password"
              placeholder={t("employeeManagement.password")}
              value={formData.password}
              onChange={handleChange}
              required
            />
          )}
          <button type="submit">{t("employeeManagement.save")}</button>
        </form>
      </div>
    </div>
  );
};

export default EmployeePopup;
