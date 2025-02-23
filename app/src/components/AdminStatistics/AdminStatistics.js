import React, { useState, useEffect } from "react";
import { Loading, BarCard, PieCard } from "../";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement  } from "chart.js";
import { useTranslation } from "react-i18next";
import "./AdminStatistics.scss";
import axios from "axios";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

/**
 * AdminStatistics component.
 * - Fetches and displays platform-wide statistics for the admin dashboard.
 * - Uses bar and pie charts to visualize user distribution and total quizzes.
 */

const AdminStatistics = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatistics();
  }, []);

  // Fetches admin dashboard statistics from the backend
  const fetchStatistics = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("http://127.0.0.1:8000/api/dashboard/admin-dashboard/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching statistics:", error);
    } finally {
      setLoading(false);
    }
  };

  // Chart data configuration for user distribution
  const userData = {
    labels: [t("admin_statistics.admins"), t("admin_statistics.companies"), t("admin_statistics.employees")],
    datasets: [
      {
        label: t("admin_statistics.users"),
        data: stats ? [stats.admins, stats.companies, stats.employees] : [0, 0, 0],
        backgroundColor: ["#4CAF50", "#FF9800", "#2196F3"],
        borderRadius: 8
      }
    ]
  };

  // Chart data configuration for total number of quizzes
  const quizData = {
    labels: [t("admin_statistics.quizzes")],
    datasets: [
      {
        label: t("admin_statistics.total_quizzes"),
        data: stats ? [stats.quizzes] : [0],
        backgroundColor: ["#9C27B0"],
        hoverBackgroundColor: ["#6A1B9A"]
      }
    ]
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="admin-statistics">
      <h2>{t("admin_statistics.platform_statistics")}</h2>

      <div className="stats-container">
        <BarCard title={t("admin_statistics.user_distribution")} data={userData} />
        <PieCard title={t("admin_statistics.total_quizzes")} data={quizData} />
      </div>
    </div>
  );
};

export default AdminStatistics;
