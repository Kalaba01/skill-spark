import React, { useState, useEffect } from "react";
import { FaPlus, FaSearch } from "react-icons/fa";
import { TopBar, EmployeePopup, EmployeeManagementCard  } from "../index";
import { useTranslation } from "react-i18next";
import { showToast } from "../ToastNotification/ToastNotification";
import axios from "axios";
import "./EmployeeManagement.scss";

const EmployeeManagement = () => {
  const { t } = useTranslation();
  const [employees, setEmployees] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(
        "http://127.0.0.1:8000/api/user-management/employees/",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setEmployees(response.data);
    } catch (error) {
      console.error("Error fetching employees:", error);
    }
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const openPopup = (employee = null) => {
    setSelectedEmployee(employee);
    setIsPopupOpen(true);
  };

  const closePopup = () => {
    setSelectedEmployee(null);
    setIsPopupOpen(false);
  };

  const deleteEmployee = async (id) => {
    if (window.confirm(t("employeeManagement.confirmDelete"))) {
      try {
        const token = localStorage.getItem("access_token");
        await axios.delete(
          `http://127.0.0.1:8000/api/user-management/employees/${id}/`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        showToast(t("employeeManagement.deleteSuccess"), "success");
        fetchEmployees();
      } catch (error) {
        console.error("Error deleting employee:", error);
        showToast(t("employeeManagement.error"), "error");
      }
    }
  };

  const filteredEmployees = employees.filter((emp) =>
    `${emp.first_name} ${emp.last_name}`
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  return (
    <>
      <TopBar />
      <div className="employee-management">
        <h1>{t("employeeManagement.title")}</h1>

        <div className="toolbar">
          <div className="search-container">
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder={t("employeeManagement.searchPlaceholder")}
              value={searchQuery}
              onChange={handleSearch}
            />
          </div>

          <button className="add-btn" onClick={() => openPopup()}>
            <FaPlus /> {t("employeeManagement.addEmployee")}
          </button>
        </div>

        <div className="employee-list">
          {filteredEmployees.length > 0 ? (
            filteredEmployees.map((employee) => (
              <EmployeeManagementCard
                key={employee.id}
                employee={employee}
                onEdit={openPopup}
                onDelete={deleteEmployee}
              />
            ))
          ) : (
            <p className="no-results">{t("employeeManagement.noResults")}</p>
          )}
        </div>

        {isPopupOpen && (
          <EmployeePopup
            employee={selectedEmployee}
            onClose={closePopup}
            refresh={fetchEmployees}
          />
        )}
      </div>
    </>
  );
};

export default EmployeeManagement;
