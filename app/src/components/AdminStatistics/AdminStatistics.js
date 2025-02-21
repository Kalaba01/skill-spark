import React, { useState, useEffect } from "react";
import { Loading, BarCard, PieCard } from "../";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement  } from "chart.js";
import { useTranslation } from "react-i18next";
import "./AdminStatistics.scss";
import axios from "axios";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

const AdminStatistics = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStatistics();
  }, []);

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

  if (loading) {
    return <Loading />;
  }

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
