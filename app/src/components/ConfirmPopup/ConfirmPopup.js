import React from "react";
import { useTranslation } from "react-i18next";
import "./ConfirmPopup.scss";

const ConfirmPopup = ({ message, onConfirm, onCancel }) => {
  const { t } = useTranslation();

  return (
    <div className="confirm-popup-overlay" onClick={onCancel}>
      <div className="confirm-popup-content" onClick={(e) => e.stopPropagation()}>
        <p>{message}</p>
        <div className="confirm-popup-actions">
          <button className="confirm-btn" onClick={onConfirm}>{t("confirmPopup.yes")}</button>
          <button className="cancel-btn" onClick={onCancel}>{t("confirmPopup.no")}</button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmPopup;
