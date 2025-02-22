import React, { useEffect, useState } from "react";
import { Loading, DonutCard } from "../";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./EmployeeStatistics.scss";

const EmployeeStatistics = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://localhost:8000/api/dashboard/employee-dashboard/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setStats(response.data);
      } catch (error) {
        console.error("Error fetching employee statistics:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const truncateText = (text, maxLength = 50) => {
    if (!text) return "";
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
  };

  if (loading) {
    return <Loading />
  }

  return (
    <div className="employee-statistics">
      <h2>{t("employee_statistics.dashboard")}</h2>

      <div className="stats-grid">
        <DonutCard
          title={t("employee_statistics.quiz_progress")}
          data={{
            labels: [t("employee_statistics.passed"), t("employee_statistics.remaining")],
            datasets: [{
              data: [stats.passed_quizzes, stats.total_quizzes - stats.passed_quizzes],
              backgroundColor: ["#4CAF50", "#E0E0E0"]
            }]
          }}
        />

        {(stats.last_quiz.title || stats.recommended_quiz.title) && (
          <div className="stat-card quiz-summary">
            <h3>{t("employee_statistics.quiz_summary")}</h3>
            {stats.last_quiz.title && (
              <div className="quiz-info">
                <h4>{t("employee_statistics.last_quiz_passed")}:</h4>
                <p>{truncateText(stats.last_quiz.title, 40)}</p>
                <span className="quiz-date">{t("employee_statistics.date")}: {stats.last_quiz.date}</span>
              </div>
            )}
            
            {stats.recommended_quiz?.title && (
              <div className="quiz-info recommended">
                <h4>{t("employee_statistics.recommended_quiz")}:</h4>
                <p>{truncateText(stats.recommended_quiz.title, 40)}</p>
                {stats.recommended_quiz.description && (
                    <span className="quiz-description">{truncateText(stats.recommended_quiz.description, 100)}</span>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default EmployeeStatistics;
