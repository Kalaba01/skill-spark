import React from "react";
import { TopBar, CompanyStatistics } from "../index";
import "./Company.scss";

function Company() {
    return(
        <>
            <TopBar />
            <div className="company-dashboard">
                <CompanyStatistics />
            </div>
        </>
    )
}

export default Company;
