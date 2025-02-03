import React from "react";
import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { LandingPage } from "../components/index";

const RedirectHome = () => {
  const token = localStorage.getItem("access_token");

  if (token) {
    try {
      const decoded = jwtDecode(token);
      const userRole = decoded.user.role;

      if (userRole === "admin") return <Navigate to="/admin" replace />;
      if (userRole === "company") return <Navigate to="/company" replace />;
      if (userRole === "employee") return <Navigate to="/employee" replace />;
    } catch (error) {
      console.error("Error decoding JWT:", error);
      localStorage.removeItem("access_token");
    }
  }

  return <LandingPage />;
};

export default RedirectHome;
