import React, { useState, useEffect } from "react";
import { FaSearch, FaFilter, FaCalendarAlt } from "react-icons/fa";
import { Loading, TopBar } from "../";
import axios from "axios";
import { useTranslation } from "react-i18next";
import "./EmployeePassedQuizzes.scss";

const EmployeePassedQuizzes = () => {
  const { t } = useTranslation();
  const [quizzes, setQuizzes] = useState([]);
  const [filteredQuizzes, setFilteredQuizzes] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [difficultyFilter, setDifficultyFilter] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPassedQuizzes();
  }, []);

  const fetchPassedQuizzes = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("http://127.0.0.1:8000/api/quizzes/employee-passed-quizzes/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setQuizzes(response.data);
      setFilteredQuizzes(response.data);
    } catch (error) {
      console.error("Error fetching passed quizzes:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    const query = e.target.value.toLowerCase();
    setSearchQuery(query);
    filterQuizzes(query, difficultyFilter);
  };

  const handleFilterChange = (e) => {
    const difficulty = e.target.value;
    setDifficultyFilter(difficulty);
    filterQuizzes(searchQuery, difficulty);
  };

  const filterQuizzes = (query, difficulty) => {
    let filtered = quizzes.filter((quiz) =>
      quiz.quiz.title.toLowerCase().includes(query)
    );

    if (difficulty !== "all") {
      filtered = filtered.filter((quiz) => quiz.quiz.difficulty === difficulty);
    }

    setFilteredQuizzes(filtered);
  };

  if (loading) {
    return (
      <>
        <TopBar />
        <Loading />
      </>
    );
  }

  return (
    <>
      <TopBar />
      <div className="employee-passed-quizzes">
        <h1>{t("employeePassedQuizzes.title")}</h1>

        <div className="toolbar">
          <div className="search-container">
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder={t("employeePassedQuizzes.searchPlaceholder")}
              value={searchQuery}
              onChange={handleSearch}
            />
          </div>

          <div className="filter-container">
            <FaFilter className="filter-icon" />
            <select value={difficultyFilter} onChange={handleFilterChange}>
              <option value="all">{t("employeePassedQuizzes.all")}</option>
              <option value="easy">{t("employeePassedQuizzes.easy")}</option>
              <option value="medium">{t("employeePassedQuizzes.medium")}</option>
              <option value="hard">{t("employeePassedQuizzes.hard")}</option>
            </select>
          </div>
        </div>

        <div className="quiz-list">
          {filteredQuizzes.length > 0 ? (
            filteredQuizzes.map((quizData) => (
              <div key={quizData.id} className="quiz-card">
                <div className="quiz-header">
                  <h3>{quizData.quiz.title}</h3>
                </div>
                <p className="description">{quizData.quiz.description}</p>
                
                <div className="quiz-footer">
                  <span className="passed-date">
                    <FaCalendarAlt className="calendar-icon" /> {t("employeePassedQuizzes.passedDate")}: {quizData.passed_date}
                  </span>
                  <span className={`difficulty-badge ${quizData.quiz.difficulty}`}>
                    {t(`employeePassedQuizzes.${quizData.quiz.difficulty}`)}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <p className="no-results">{t("employeePassedQuizzes.noResults")}</p>
          )}
        </div>
      </div>
    </>
  );
};

export default EmployeePassedQuizzes;
