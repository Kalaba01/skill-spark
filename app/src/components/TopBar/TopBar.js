import React from "react";
import { FaUserCircle, FaSun, FaMoon, FaBell, FaComments, FaSignOutAlt } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { toggleTheme } from "../../store/themeSlice";
import { Language } from "../index";
import { jwtDecode } from "jwt-decode";
import "./TopBar.scss";

function TopBar({ openLogin }) {
  const dispatch = useDispatch();
  const theme = useSelector((state) => state.theme.theme);

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
      <div className="logo">SkillSpark</div>

      <div className="top-bar-icons">
        {!userRole ? (
          <>
            <FaUserCircle size={24} className="icon" onClick={openLogin} />
            {theme === "light" ? (
              <FaMoon size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
            ) : (
              <FaSun size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
            )}
            <Language />
          </>
        ) : (
          <>
            <FaBell size={24} className="icon" />
            <FaComments size={24} className="icon" />
            {theme === "light" ? (
              <FaMoon size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
            ) : (
              <FaSun size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
            )}
            <Language />
            <FaSignOutAlt size={24} className="icon logout-icon" />
          </>
        )}
      </div>
    </header>
  );
}

export default TopBar;
