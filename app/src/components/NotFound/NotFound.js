import React from "react";
import { useNavigate } from "react-router-dom";
import { FaExclamationTriangle, FaArrowLeft } from "react-icons/fa";
import { TopBar } from "../index";
import { useTranslation } from "react-i18next";
import "./NotFound.scss";

const NotFound = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  return (
    <>
      <TopBar variant="notfound" />

      <div className="not-found">
        <div className="not-found-content">
          <FaExclamationTriangle className="not-found-icon" />
          <h1>404</h1>
          <h2>{t("notFound.title")}</h2>
          <p>{t("notFound.description")}</p>
          <button onClick={() => navigate("/")}>
            <FaArrowLeft className="button-icon" /> {t("notFound.button")}
          </button>
        </div>
      </div>
    </>
  );
};

export default NotFound;
