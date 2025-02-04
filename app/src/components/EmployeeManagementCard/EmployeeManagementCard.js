import React from "react";
import { FaEdit, FaTrash } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import "./EmployeeManagementCard.scss";

const EmployeeManagementCard = ({ employee, onEdit, onDelete }) => {
  const { t } = useTranslation();

  return (
    <div className="employee-card">
      <div className="employee-info">
        <p><strong>{t("employeeManagementCard.firstName")}:</strong> {employee.first_name}</p>
        <p><strong>{t("employeeManagementCard.lastName")}:</strong> {employee.last_name}</p>
        <p><strong>Email:</strong> {employee.email}</p>
      </div>
      <div className="actions">
        <FaEdit className="edit-icon" onClick={() => onEdit(employee)} />
        <FaTrash className="delete-icon" onClick={() => onDelete(employee.id)} />
      </div>
    </div>
  );
};

export default EmployeeManagementCard;
