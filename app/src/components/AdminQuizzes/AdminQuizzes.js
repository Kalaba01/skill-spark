import React, { useState, useEffect } from "react";
import { FaSearch, FaFilter } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import { Loading, TopBar } from "../";
import axios from "axios";
import "./AdminQuizzes.scss";

/**
 * AdminQuizzes component.
 * - Displays a list of all quizzes across all companies.
 * - Provides search and filter functionality.
 * - Fetches quiz data from the backend on component mount.
 */

const AdminQuizzes = () => {
  const { t } = useTranslation();
  const [quizzes, setQuizzes] = useState([]);
  const [filteredQuizzes, setFilteredQuizzes] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCompany, setSelectedCompany] = useState("all");
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuizzes();
  }, []);

  // Fetches all quizzes from the backend
  const fetchQuizzes = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(
        "http://127.0.0.1:8000/api/quizzes/admin/all-quizzes/",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setQuizzes(response.data);
      setFilteredQuizzes(response.data);
      extractUniqueCompanies(response.data);
    } catch (error) {
      console.error("Error fetching quizzes:", error);
    } finally {
      setLoading(false);
    }
  };

  // Extracts unique company names from the quiz data
  const extractUniqueCompanies = (quizzesData) => {
    const uniqueCompanies = [
      ...new Set(quizzesData.map((quiz) => quiz.company_name)),
    ];
    setCompanies(uniqueCompanies);
  };

  // Handles search input change and filters quizzes based on the query
  const handleSearch = (e) => {
    const query = e.target.value.toLowerCase();
    setSearchQuery(query);
    filterQuizzes(query, selectedCompany);
  };

  // Handles company filter change and filters quizzes accordingly
  const handleCompanyFilter = (e) => {
    const company = e.target.value;
    setSelectedCompany(company);
    filterQuizzes(searchQuery, company);
  };

  // Filters quizzes based on search query and selected company
  const filterQuizzes = (query, company) => {
    let filtered = quizzes.filter((quiz) =>
      quiz.title.toLowerCase().includes(query)
    );

    if (company !== "all") {
      filtered = filtered.filter((quiz) => quiz.company_name === company);
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
      <div className="admin-quizzes">
        <h1>{t("adminQuizzes.title")}</h1>

        <div className="toolbar">
          <div className="search-container">
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder={t("adminQuizzes.searchPlaceholder")}
              value={searchQuery}
              onChange={handleSearch}
            />
          </div>

          <div className="filter-container">
            <FaFilter className="filter-icon" />
            <select value={selectedCompany} onChange={handleCompanyFilter}>
              <option value="all">{t("adminQuizzes.allCompanies")}</option>
              {companies.map((company, index) => (
                <option key={index} value={company}>
                  {company}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="quiz-list">
          {filteredQuizzes.length > 0 ? (
            filteredQuizzes.map((quiz) => (
              <div key={quiz.id} className="quiz-card">
                <h3>{quiz.title}</h3>
                <p className="company">{quiz.company_name}</p>
                <p className="description">{quiz.description}</p>
                <div className="quiz-footer">
                  <span className={`difficulty ${quiz.difficulty}`}>
                    {t(`adminQuizzes.${quiz.difficulty}`)}
                  </span>
                  <span className="duration">
                    {quiz.duration} {t("adminQuizzes.minutes")}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <p className="no-results">{t("adminQuizzes.noResults")}</p>
          )}
        </div>
      </div>
    </>
  );
};

export default AdminQuizzes;
