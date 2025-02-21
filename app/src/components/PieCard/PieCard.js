import React from "react";
import { Pie } from "react-chartjs-2";
import "./PieCard.scss";

const PieCard = ({ title, data }) => {
  return (
    <div className="stat-card">
      <h3>{title}</h3>
      <Pie className="pie-chart" data={data} options={{ responsive: true, plugins: { legend: { position: "bottom" } } }} />
    </div>
  );
};

export default PieCard;
