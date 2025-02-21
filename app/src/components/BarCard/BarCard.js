import React from "react";
import { Bar } from "react-chartjs-2";
import "./BarCard.scss";

const BarCard = ({ title, data }) => {
  return (
    <div className="stat-card">
      <h3>{title}</h3>
      <Bar data={data} options={{ responsive: true, plugins: { legend: { display: false } } }} />
    </div>
  );
};

export default BarCard;
