import React, { useState } from "react";
import { FaBars, FaTimes } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./HamburgerMenu.scss";

function HamburgerMenu({ userRole }) {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  const menuItems = {
    admin: [
      { label: "Dashboard", path: "/admin" },
      { label: "Manage Users", path: "/admin/users" },
      { label: "Settings", path: "/admin/settings" }
    ],
    company: [
      { label: "Employees Management", path: "/company/employees-management" },
      { label: "Settings", path: "/company/settings" }
    ],
    employee: [
      { label: "My Dashboard", path: "/employee" },
      { label: "My Training", path: "/employee/training" },
      { label: "Profile", path: "/employee/profile" }
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
