import React from "react";
import { FaUserCircle, FaBell, FaComments, FaSignOutAlt } from "react-icons/fa";
import { Language, Theme, HamburgerMenu } from "../index";
import { jwtDecode } from "jwt-decode";
import "./TopBar.scss";

function TopBar({ openLogin }) {
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
      {userRole && <HamburgerMenu userRole={userRole} />}

      <div className="logo">SkillSpark</div>

      <div className="top-bar-icons">
        {!userRole ? (
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
            <FaSignOutAlt size={24} className="icon logout-icon" />
          </>
        )}
      </div>
    </header>
  );
}

export default TopBar;
