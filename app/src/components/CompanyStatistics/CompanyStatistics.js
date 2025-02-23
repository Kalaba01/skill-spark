import React, { useState, useEffect } from "react";
import { Loading, PieCard, DonutCard } from "../";
import { Chart as ChartJS, CategoryScale, LinearScale, ArcElement, Title, Tooltip, Legend } from "chart.js";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./CompanyStatistics.scss";

ChartJS.register(CategoryScale, LinearScale, ArcElement, Title, Tooltip, Legend);

/**
 * CompanyStatistics component.
 * - Fetches and displays company-specific statistics.
 * - Uses pie and donut charts to visualize employee count and total quizzes.
 */

const CompanyStatistics = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatistics();
  }, []);

  // Fetches company dashboard statistics from the backend
  const fetchStatistics = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("http://127.0.0.1:8000/api/dashboard/company-dashboard/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching statistics:", error);
    } finally {
      setLoading(false);
    }
  };

  // Chart data configuration for employee distribution
  const employeeData = {
    labels: [t("company_statistics.employees")],
    datasets: [
      {
        label: t("company_statistics.total_employees"),
        data: stats ? [stats.employees] : [0],
        backgroundColor: ["#2196F3"],
        hoverBackgroundColor: ["#1976D2"]
      }
    ]
  };

  // Chart data configuration for total number of quizzes
  const quizData = {
    labels: [t("company_statistics.quizzes")],
    datasets: [
      {
        label: t("company_statistics.total_quizzes"),
        data: stats ? [stats.quizzes] : [0],
        backgroundColor: ["#FF9800"],
        hoverBackgroundColor: ["#F57C00"]
      }
    ]
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="company-statistics">
      <h2>{t("company_statistics.company_statistics")}</h2>
      <div className="stats-container">
        <PieCard title={t("company_statistics.employee_distribution")} data={employeeData} />
        <DonutCard title={t("company_statistics.total_quizzes")} data={quizData} />
      </div>
    </div>
  );
};

export default CompanyStatistics;
