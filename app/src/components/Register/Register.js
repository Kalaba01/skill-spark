import React, { useState } from "react";
import axios from "axios";
import "./Register.scss";

function Register({ isOpen, onClose, switchToLogin }) {
  const [formData, setFormData] = useState({
    company_name: "",
    email: "",
    password: "",
    confirm_password: ""
  });

  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match!");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/auth/register/", {
        company_name: formData.company_name,
        email: formData.email,
        password: formData.password
      });

      setSuccessMessage(response.data.message);
      setError(null);

      setFormData({
        company_name: "",
        email: "",
        password: "",
        confirm_password: ""
      });

      setTimeout(() => {
        switchToLogin();
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="register-overlay" onClick={onClose}>
      <div className="register-popup" onClick={(e) => e.stopPropagation()}>
        <h2>Register</h2>

        {/* Prikaz uspešne poruke */}
        {successMessage && <p className="success-message">{successMessage}</p>}

        {/* Prikaz greške */}
        {error && <p className="error-message">{error}</p>}

        <form onSubmit={handleSubmit}>
          <label>Company Name</label>
          <input
            type="text"
            name="company_name"
            placeholder="Enter company name"
            required
            value={formData.company_name}
            onChange={handleChange}
          />

          <label>Email</label>
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            required
            value={formData.email}
            onChange={handleChange}
          />

          <label>Password</label>
          <input
            type="password"
            name="password"
            placeholder="Create a password"
            required
            value={formData.password}
            onChange={handleChange}
          />

          <label>Confirm Password</label>
          <input
            type="password"
            name="confirm_password"
            placeholder="Confirm your password"
            required
            value={formData.confirm_password}
            onChange={handleChange}
          />

          <button type="submit" className="register-btn">Register</button>
        </form>

        <p className="login-link">
          Already have an account? <span onClick={switchToLogin}>Login</span>
        </p>

        <button className="close-btn" onClick={onClose}>&times;</button>
      </div>
    </div>
  );
}

export default Register;
