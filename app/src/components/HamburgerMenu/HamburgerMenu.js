import React, { useState } from "react";
import { FaBars, FaTimes } from "react-icons/fa";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import "./HamburgerMenu.scss";

function HamburgerMenu({ userRole }) {
  const { t } = useTranslation();
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const menuItems = {
    admin: [
      { label: t("hamburgerMenu.users_management"), path: "/admin/users-management" }
    ],
    company: [
      { label: t("hamburgerMenu.employees_management"), path: "/company/employees-management" },
      { label: t("hamburgerMenu.quizzes"), path: "/company/quizzes" }
    ],
    employee: [
      { label: t("hamburgerMenu.profile"), path: "/employee/profile" },
      { label: t("hamburgerMenu.quizzes"), path: "/employee/quizzes" },
      { label: t("hamburgerMenu.passed_quizzes"), path: "/employee/passed-quizzes" },
    ]
  };

  return (
    <div className="hamburger-menu">
      <div className="menu-icon" onClick={toggleMenu}>
        {menuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
      </div>

      <nav className={`menu-content ${menuOpen ? "open" : ""}`}>
        <ul>
          {menuItems[userRole]?.map((item, index) => (
            <li key={index}>
              <Link to={item.path} onClick={toggleMenu}>
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

export default HamburgerMenu;
