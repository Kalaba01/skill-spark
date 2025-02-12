import React from "react";
import { useTranslation } from "react-i18next";
import "./QuizCard.scss";

const QuizCard = ({ quiz, actions }) => {
  const { t } = useTranslation();

  const truncateText = (text, maxLength) => {
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
  };

  return (
    <div className="quiz-card">
      <h3>{truncateText(quiz.title, 25)}</h3>
      <p>{truncateText(quiz.description, 50)}</p>
      <span className={`difficulty ${quiz.difficulty}`}>
        {t(`quizzes.difficulty_${quiz.difficulty}`)}
      </span>
      <p>
        <strong>{t("quizzes.duration")}:</strong> {quiz.duration} min
      </p>

      <div className="actions">{actions}</div>
    </div>
  );
};

export default QuizCard;
