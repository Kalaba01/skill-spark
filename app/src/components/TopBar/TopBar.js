import React from "react";
import { FaUserCircle, FaBell, FaComments } from "react-icons/fa";
import { Language, Theme, HamburgerMenu, Logout } from "../index";
import { jwtDecode } from "jwt-decode";
import "./TopBar.scss";

function TopBar({ openLogin, variant = "default" }) {
  const accessToken = localStorage.getItem("access_token");
  let userRole = null;

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

      <div className="logo">SkillSpark</div>

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
            <FaBell size={24} className="icon" />
            <FaComments size={24} className="icon" />
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
