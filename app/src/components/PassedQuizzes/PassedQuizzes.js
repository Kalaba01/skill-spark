import React from "react";
import { useTranslation } from "react-i18next";
import { FaTimes } from "react-icons/fa";
import "./PassedQuizzes.scss";

const PassedQuizzes = ({ quizzes = [], onClose }) => {
  const { t } = useTranslation();

  return (
    <div className="passed-quizzes-modal">
      <div className="modal-content">
        <button className="close-btn" onClick={onClose}>
          <FaTimes />
        </button>
        <h2>{t("passedQuizzes.title")}</h2>
        {quizzes.length > 0 ? (
          <ul>
            {quizzes.map((quiz) => (
              <li key={quiz.id}>{quiz.title}</li>
            ))}
          </ul>
        ) : (
          <p>{t("passedQuizzes.noPassedQuizzes")}</p>
        )}
      </div>
    </div>
  );
};

export default PassedQuizzes;
