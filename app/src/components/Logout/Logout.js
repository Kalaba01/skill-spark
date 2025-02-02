import React from "react";
import { useNavigate } from "react-router-dom";
import { FaSignOutAlt } from "react-icons/fa";
import "./Logout.scss";

const Logout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    navigate("/", { replace: true });
  };

  return (
    <FaSignOutAlt size={24} className="icon logout-icon" onClick={handleLogout} />
  );
};

export default Logout;
