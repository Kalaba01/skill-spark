import React from "react";
import { useNavigate } from "react-router-dom";
import { FaExclamationTriangle } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import { TopBar } from "../index";
import "./Unauthorized.scss";

const Unauthorized = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <>
      <TopBar variant="unauthorized" />

      <div className="unauthorized">
        <FaExclamationTriangle className="warning-icon" />
        <h1>403</h1>
        <h2>{t("unauthorized.title")}</h2>
        <p>{t("unauthorized.description")}</p>
        <button onClick={() => navigate("/")}>{t("unauthorized.button")}</button>
      </div>
    </>
  );
};

export default Unauthorized;
