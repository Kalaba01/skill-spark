import React from "react";
import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { LandingPage } from "../components/index";

/**
 * RedirectHome middleware
 *
 * - Redirects authenticated users to their respective dashboards based on role.
 * - If no valid authentication token is found, renders the LandingPage.
 * - Handles invalid or corrupted tokens safely.
 */

const RedirectHome = () => {
  const token = localStorage.getItem("access_token");

  if (token) {
    try {
      const decoded = jwtDecode(token);
      const userRole = decoded.user.role;

      // Redirect users based on their assigned roles
      if (userRole === "admin") return <Navigate to="/admin" replace />;
      if (userRole === "company") return <Navigate to="/company" replace />;
      if (userRole === "employee") return <Navigate to="/employee" replace />;
    } catch (error) {
      console.error("Error decoding JWT:", error);
      localStorage.removeItem("access_token"); // Remove invalid token
    }
  }

  // If no valid token is found, show the Landing Page
  return <LandingPage />;
};

export default RedirectHome;
