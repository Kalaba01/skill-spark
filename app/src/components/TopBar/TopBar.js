import React from "react";
import { FaUserCircle } from "react-icons/fa";
import { Language, Theme, HamburgerMenu, Logout } from "../index";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import "./TopBar.scss";

/**
 * TopBar Component
 *
 * - Displays the top navigation bar of the application.
 * - Includes the logo, menu, language settings, theme switch, and login/logout options.
 */

function TopBar({ openLogin, variant = "default" }) {
  const navigate = useNavigate();
  const accessToken = localStorage.getItem("access_token");
  let userRole = null;

  // Decode JWT token to get the user role
  if (accessToken) {
    try {
      const decoded = jwtDecode(accessToken);
      userRole = decoded.user.role;
    } catch (error) {
      console.error("Error decoding JWT:", error);
    }
  }

  return (
    <header className="top-bar">
      {(variant !== "unauthorized" && variant !== "notfound") && userRole && <HamburgerMenu userRole={userRole} />}

      <div className="logo-container">
        <img src="/logo.png" alt="SkillSpark Logo" className="logo-img" onClick={() => navigate("/")} />
        <span className="logo-text">SkillSpark</span>
      </div>

      <div className="top-bar-icons">
        {(variant === "unauthorized" || variant === "notfound") ? (
          <>
            <Theme />
            <Language />
          </>
        ) : !userRole ? (
          <>
            <FaUserCircle size={24} className="icon" onClick={openLogin} />
            <Theme />
            <Language />
          </>
        ) : (
          <>
            <Theme />
            <Language />
            <Logout />
          </>
        )}
      </div>
    </header>
  );
}

export default TopBar;
