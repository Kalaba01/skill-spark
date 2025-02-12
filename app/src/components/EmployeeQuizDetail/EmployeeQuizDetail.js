import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { TopBar } from "../";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./EmployeeQuizDetail.scss";

const EmployeeQuizDetail = () => {
  const { t } = useTranslation();
  const { id } = useParams();
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          `http://127.0.0.1:8000/api/quizzes/${id}/detail/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setQuiz(response.data);
      } catch (error) {
        console.error("Error fetching quiz details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuiz();
  }, [id]);

  if (loading) {
    return (
      <div className="loading-container">
        <p>{t("employee_quiz_detail.loading")}</p>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="error-container">
        <p>{t("employee_quiz_detail.not_found")}</p>
      </div>
    );
  }

  return (
    <>
      <TopBar />
      <div className="quiz-detail-container">
        <h1 className="quiz-title">{quiz.title}</h1>

        <p className="quiz-description">
          <strong>{t("employee_quiz_detail.description")}:</strong> {quiz.description}
        </p>

        <div className="quiz-info">
          <p>
            <strong>{t("employee_quiz_detail.difficulty")}:</strong>{" "}
            <span className={`difficulty ${quiz.difficulty}`}>
              {t(`employee_quiz_detail.difficulty_${quiz.difficulty}`)}
            </span>
          </p>
          <p>
            <strong>{t("employee_quiz_detail.duration")}:</strong>{" "}
            {quiz.duration} min
          </p>
          <p>
            <strong>{t("employee_quiz_detail.questions_count")}:</strong>{" "}
            {quiz.question_count}
          </p>
        </div>

        <button className="start-quiz-btn">{t("employee_quiz_detail.start_quiz")}</button>
      </div>
    </>
  );
};

export default EmployeeQuizDetail;
