import React, { useState, useEffect } from "react";
import { TopBar, Loading, EmployeeProfileEdit } from "../index";
import { FaUserEdit } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./EmployeeProfile.scss";

/**
 * EmployeeProfile component.
 * - Displays the employee's profile details.
 * - Allows editing of profile information.
 * - Fetches profile data from the API on component mount.
 */

const EmployeeProfile = () => {
  const { t } = useTranslation();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  // Fetches the employee's profile data from the backend
  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("http://127.0.0.1:8000/api/user-management/employee-profile/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProfile(response.data);
    } catch (error) {
      console.error("Error fetching profile:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <>
        <TopBar />
        <Loading />
      </>
    );
  }

  return (
    <>
      <TopBar />
      <div className="profile-container">
        <h1>{t("employeeProfile.title")}</h1>
        <div className="profile-card">
          <div className="profile-avatar">
            <FaUserEdit className="avatar-icon" />
          </div>
          <div className="profile-info">
            <p><strong>{t("employeeProfile.firstName")}:</strong> {profile?.first_name}</p>
            <p><strong>{t("employeeProfile.lastName")}:</strong> {profile?.last_name}</p>
            <p><strong>{t("employeeProfile.email")}:</strong> {profile?.email}</p>
            <p><strong>{t("employeeProfile.workingAt")}:</strong> {profile?.working_at}</p>
          </div>
        </div>
        <button className="edit-btn" onClick={() => setIsEditing(true)}>
            {t("employeeProfile.editProfile")}
        </button>
      
        {/* Profile Edit Popup */}
        {isEditing && (
          <EmployeeProfileEdit
            profile={profile}
            onClose={() => setIsEditing(false)}
            refreshProfile={fetchProfile}
          />
        )}
      
      </div>
    </>
  );
};

export default EmployeeProfile;
