import React from "react";
import { TopBar, AdminStatistics } from "../";
import "./Admin.scss";

function Admin() {
  return (
    <>
      <TopBar />
      <div className="admin-dashboard">
        <AdminStatistics />
      </div>
    </>
  );
}

export default Admin;
