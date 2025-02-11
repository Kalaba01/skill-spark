import React, { useState, useEffect } from "react";
import { TopBar } from "../";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import axios from "axios";
import "./EmployeeQuizzes.scss";

const EmployeeQuizzes = () => {
  const { t } = useTranslation();
  const [quizzes, setQuizzes] = useState([]);
  const [filteredQuizzes, setFilteredQuizzes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [durationFilter, setDurationFilter] = useState("");

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/quizzes/employee-quizzes/",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setQuizzes(response.data);
        setFilteredQuizzes(response.data);
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    };

    fetchQuizzes();
  }, []);

  useEffect(() => {
    let filtered = quizzes.filter((quiz) =>
      quiz.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (durationFilter) {
      filtered = filtered.filter((quiz) => {
        if (durationFilter === "<10") return quiz.duration < 10;
        if (durationFilter === "10-30")
          return quiz.duration >= 10 && quiz.duration <= 30;
        if (durationFilter === "30+") return quiz.duration > 30;
        return true;
      });
    }

    setFilteredQuizzes(filtered);
  }, [searchTerm, durationFilter, quizzes]);

  return (
    <>
    <TopBar />
      <div className="employee-quizzes">
        <h1>{t("employee_quizzes.title")}</h1>

        {/* Toolbox */}
        <div className="toolbox">
          <input
            type="text"
            placeholder={t("employee_quizzes.search_placeholder")}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

          <select
            value={durationFilter}
            onChange={(e) => setDurationFilter(e.target.value)}
          >
            <option value="">{t("employee_quizzes.all_durations")}</option>
            <option value="<10">{t("employee_quizzes.duration_short")}</option>
            <option value="10-30">
              {t("employee_quizzes.duration_medium")}
            </option>
            <option value="30+">{t("employee_quizzes.duration_long")}</option>
          </select>
        </div>

        {/* Quiz Cards */}
        <div className="quiz-list">
          {filteredQuizzes.length > 0 ? (
            filteredQuizzes.map((quiz) => (
              <div key={quiz.id} className="quiz-card">
                <h2>{quiz.title}</h2>
                <p>{quiz.description}</p>
                <p>
                  <strong>{t("employee_quizzes.difficulty")}:</strong>{" "}
                  {quiz.difficulty}
                </p>
                <p>
                  <strong>{t("employee_quizzes.duration")}:</strong>{" "}
                  {quiz.duration} min
                </p>
                <Link to={`/quiz/${quiz.id}`} className="view-btn">
                  {t("employee_quizzes.view_button")}
                </Link>
              </div>
            ))
          ) : (
            <p className="no-quizzes">{t("employee_quizzes.no_quizzes")}</p>
          )}
        </div>
      </div>
    </>
  );
};

export default EmployeeQuizzes;
