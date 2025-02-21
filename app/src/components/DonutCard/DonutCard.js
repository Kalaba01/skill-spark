import React from "react";
import { Doughnut } from "react-chartjs-2";
import "./DonutCard.scss";

const DonutCard = ({ title, data }) => {
  return (
    <div className="stat-card">
      <h3>{title}</h3>
      <Doughnut className="donut-chart" data={data} options={{ responsive: true, plugins: { legend: { position: "bottom" } } }} />
    </div>
  );
};

export default DonutCard;
