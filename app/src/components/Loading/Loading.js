import React from "react";
import { useTranslation } from "react-i18next";
import "./Loading.scss";

const Loading = () => {
  const { t } = useTranslation();

  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>{t("loading.text")}</p>
    </div>
  );
};

export default Loading;
