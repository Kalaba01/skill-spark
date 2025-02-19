import React, { useState, useEffect } from "react";
import { TopBar, Loading, CompanyProfileEdit } from "../";
import { FaBuilding, FaEnvelope, FaUsers, FaClipboardList, FaEdit } from "react-icons/fa";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./CompanyProfile.scss";

const CompanyProfile = () => {
  const { t } = useTranslation();
  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetchCompanyProfile();
  }, []);

  const fetchCompanyProfile = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get("http://127.0.0.1:8000/api/user-management/company-profile/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setCompany(response.data);
    } catch (error) {
      console.error("Error fetching company profile:", error);
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
      <div className="company-profile">
        <div className="profile-card">
          <h1>{t("companyProfile.title")}</h1>

          {company ? (
            <div className="company-details">
              <div className="company-info">
                <div className="info-item">
                  <FaBuilding className="icon" />
                  <div className="info-text">
                    <h3>{t("companyProfile.companyName")}</h3>
                    <p>{company.company_name}</p>
                  </div>
                </div>

                <div className="info-item">
                  <FaEnvelope className="icon" />
                  <div className="info-text">
                    <h3>{t("companyProfile.email")}</h3>
                    <p>{company.email}</p>
                  </div>
                </div>

                <div className="info-item">
                  <FaUsers className="icon" />
                  <div className="info-text">
                    <h3>{t("companyProfile.employees")}</h3>
                    <p>{company.employee_count}</p>
                  </div>
                </div>

                <div className="info-item">
                  <FaClipboardList className="icon" />
                  <div className="info-text">
                    <h3>{t("companyProfile.quizzesCreated")}</h3>
                    <p>{company.quiz_count}</p>
                  </div>
                </div>
              </div>

              <button className="edit-btn" onClick={() => setIsEditing(true)}>
                <FaEdit className="edit-icon" /> {t("companyProfile.editProfile")}
              </button>
            </div>
          ) : (
            <p className="no-data">{t("companyProfile.noData")}</p>
          )}
        </div>
      </div>

      {isEditing && (
        <CompanyProfileEdit
          company={company}
          onClose={() => setIsEditing(false)}
          refreshProfile={fetchCompanyProfile}
        />
      )}
    </>
  );
};

export default CompanyProfile;
