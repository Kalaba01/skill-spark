import React from "react";
import { useNavigate } from "react-router-dom";
import { FaSignOutAlt } from "react-icons/fa";
import "./Logout.scss";

/**
 * Logout Component
 * - Provides a logout button that removes authentication tokens from local storage.
 * - Redirects the user to the home page after logout.
 * - Uses React Router's `useNavigate` for navigation.
 */

const Logout = () => {
  const navigate = useNavigate();

  // Handles user logout
  const handleLogout = () => {
    // Removes JWT tokens from local storage
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    // Redirects the user to the homepage
    navigate("/", { replace: true });
  };

  return (
    <FaSignOutAlt size={24} className="icon logout-icon" onClick={handleLogout} />
  );
};

export default Logout;
