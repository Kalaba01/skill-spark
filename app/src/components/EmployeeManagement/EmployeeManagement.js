import React, { useState, useEffect } from "react";
import { FaPlus, FaSearch } from "react-icons/fa";
import { TopBar, EmployeePopup, UserCard, ConfirmPopup, Loading, PassedQuizzes } from "../index";
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
  const [confirmPopup, setConfirmPopup] = useState({ show: false, employeeId: null });
  const [loading, setLoading] = useState(true);
  const [passedQuizzes, setPassedQuizzes] = useState(null);

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
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async (employeeId, firstName, lastName) => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(
        `http://127.0.0.1:8000/api/user-management/employees/${employeeId}/report/`,
        {
          headers: { Authorization: `Bearer ${token}` },
          responseType: "blob", // Ovo osigurava da dobijemo fajl, a ne JSON
        }
      );

      // Kreiranje URL-a za preuzimanje fajla
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `${firstName}_${lastName}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      showToast(t("userCard.reportSuccess"), "success");
    } catch (error) {
      console.error("Error generating report:", error);
      showToast(t("userCard.reportError"), "error");
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

  const confirmDelete = (id) => {
    setConfirmPopup({ show: true, employeeId: id });
  };

  const cancelDelete = () => {
    setConfirmPopup({ show: false, employeeId: null });
  };

  const deleteEmployee = async () => {
    if (!confirmPopup.employeeId) return;
    try {
      const token = localStorage.getItem("access_token");
      await axios.delete(
        `http://127.0.0.1:8000/api/user-management/employees/${confirmPopup.employeeId}/`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      showToast(t("employeeManagement.deleteSuccess"), "success");
      fetchEmployees();
    } catch (error) {
      console.error("Error deleting employee:", error);
      showToast(t("employeeManagement.error"), "error");
    } finally {
      setConfirmPopup({ show: false, employeeId: null });
    }
  };

  const filteredEmployees = employees.filter((emp) =>
    `${emp.first_name} ${emp.last_name}`
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  if (loading) {
      return (
        <>
          <TopBar />;
          <Loading />;
        </>
      )
  }

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
              <UserCard
                key={employee.id}
                data={employee}
                fields={["first_name", "last_name", "email"]}
                onEdit={openPopup}
                onDelete={() => confirmDelete(employee.id)}
                context="employeeManagement"
                onShowPassedQuizzes={setPassedQuizzes}
                onGenerateReport={() => handleGenerateReport(employee.id, employee.first_name, employee.last_name)}
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

        {confirmPopup.show && (
          <ConfirmPopup
            message={t("employeeManagement.confirmDelete")}
            onConfirm={deleteEmployee}
            onCancel={cancelDelete}
          />
        )}

        {passedQuizzes !== null && 
          <PassedQuizzes 
            quizzes={passedQuizzes} 
            onClose={() => setPassedQuizzes(null)} 
            />
        }

      </div>
    </>
  );
};

export default EmployeeManagement;
