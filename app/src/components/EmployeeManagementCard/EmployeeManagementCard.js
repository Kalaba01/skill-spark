import React from "react";
import { FaEdit, FaTrash } from "react-icons/fa";
import "./EmployeeManagementCard.scss";

const EmployeeManagementCard = ({ employee, onEdit, onDelete }) => {
  return (
    <div className="employee-card">
      <div className="employee-info">
        <p><strong>First Name:</strong> {employee.first_name}</p>
        <p><strong>Last Name:</strong> {employee.last_name}</p>
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
