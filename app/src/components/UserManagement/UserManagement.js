import React, { useState, useEffect } from "react";
import { FaPlus, FaSearch } from "react-icons/fa";
import { TopBar, UserCard, CreateUserPopup, ConfirmPopup, Loading } from "../index";
import { useTranslation } from "react-i18next";
import { showToast } from "../ToastNotification/ToastNotification";
import axios from "axios";
import "./UserManagement.scss";

/**
 * UserManagement Component
 * - Allows an admin to manage users.
 * - Users can be searched, filtered by role, edited, and deleted.
 * - Provides a popup for adding or editing users.
 * - Fetches and displays a list of users from the backend.
 */

const UserManagement = () => {
  const { t } = useTranslation();

  const [users, setUsers] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");
  const [selectedUser, setSelectedUser] = useState(null);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [uniqueCompanies, setUniqueCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  // Fetches users from the backend and extracts unique company names
  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("http://127.0.0.1:8000/api/user-management/users/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(response.data);

      const companies = response.data
        .map((user) => user.company_name)
        .filter((company) => company !== null);
      setUniqueCompanies([...new Set(companies)]);

    } catch (error) {
      console.error("Error fetching users:", error);
    } finally {
      setLoading(false);
    }
  };

  // Handles the search input change
  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  // Handles the role filter change
  const handleRoleChange = (e) => {
    setRoleFilter(e.target.value);
  };

  const openPopup = (user = null) => {
    setSelectedUser(user);
    setIsPopupOpen(true);
  };

  const closePopup = () => {
    setSelectedUser(null);
    setIsPopupOpen(false);
  };

  // Deletes a user from the backend and refreshes the user list
  const deleteUser = async (id) => {
    try {
      const token = localStorage.getItem("access_token");
      await axios.delete(`http://127.0.0.1:8000/api/user-management/users/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      showToast(t("userManagement.deleteSuccess"), "success");
      fetchUsers();
    } catch (error) {
      console.error("Error deleting user:", error);
      showToast(t("userManagement.error"), "error");
    }
  };

  // Filters users based on search query and selected role
  const filteredUsers = users.filter((user) => {
    const matchesSearch = `${user.first_name} ${user.last_name}`.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRole = roleFilter === "all" || user.role === roleFilter;
    return matchesSearch && matchesRole;
  });

  if (loading) {
      return (
        <>
          <TopBar />
          <Loading />;
        </>
      );
    }

  return (
    <>
      <TopBar />
      <div className="user-management">
        <h1>{t("userManagement.title")}</h1>

        <div className="toolbar">
          <div className="search-container">
            <FaSearch className="search-icon" />
            <input
              type="text"
              placeholder={t("userManagement.searchPlaceholder")}
              value={searchQuery}
              onChange={handleSearch}
            />
          </div>

          <select className="role-filter" value={roleFilter} onChange={handleRoleChange}>
            <option value="all">{t("userManagement.allRoles")}</option>
            <option value="admin">{t("userManagement.admin")}</option>
            <option value="company">{t("userManagement.company")}</option>
            <option value="employee">{t("userManagement.employee")}</option>
          </select>

          <button className="add-btn" onClick={() => openPopup()}>
            <FaPlus /> {t("userManagement.addUser")}
          </button>
        </div>

        <div className="user-list">
        {filteredUsers.length > 0 ? (
            filteredUsers.map((user) => {
            let fields = [];

            if (user.role === "admin") {
                fields = ["email", "role"];
            } else if (user.role === "company") {
                fields = ["company_name", "email", "role"];
            } else if (user.role === "employee") {
                fields = ["first_name", "last_name", "email", "working_at", "role"];
            }

            return (
                <UserCard
                key={user.id}
                data={user}
                fields={fields}
                onEdit={openPopup}
                onDelete={() => setConfirmDelete(user.id)}
                context="userManagement"
                />
            );
            })
        ) : (
            <p className="no-results">{t("userManagement.noResults")}</p>
        )}
        </div>


        {isPopupOpen && <CreateUserPopup user={selectedUser} onClose={closePopup} refresh={fetchUsers} companies={uniqueCompanies} />}
        {confirmDelete && (
          <ConfirmPopup
            message={t("userManagement.confirmDelete")}
            onConfirm={() => {
              deleteUser(confirmDelete);
              setConfirmDelete(null);
            }}
            onCancel={() => setConfirmDelete(null)}
          />
        )}
      </div>
    </>
  );
};

export default UserManagement;
