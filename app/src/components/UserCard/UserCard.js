import React from "react";
import { FaEdit, FaTrash } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import "./UserCard.scss";

const UserCard = ({ data, fields, onEdit, onDelete, context }) => {
  const { t } = useTranslation();

  const translationMap = {
    first_name: `${context}.firstName`,
    last_name: `${context}.lastName`,
    email: `${context}.email`,
    role: `${context}.role`,
    company_name: `${context}.companyName`,
    working_at: `${context}.workingAt`
  };

  return (
    <div className="user-card">
      <div className="user-info">
        {fields.map((field) => (
          <p key={field}>
            <strong>{t(translationMap[field])}:</strong> {data[field] || "N/A"}
          </p>
        ))}
      </div>
      <div className="actions">
        <FaEdit className="edit-icon" onClick={() => onEdit(data)} />
        <FaTrash className="delete-icon" onClick={() => onDelete(data.id)} />
      </div>
    </div>
  );
};

export default UserCard;
