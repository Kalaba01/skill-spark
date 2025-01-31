import React, { useState } from "react";
import axios from "axios";
import { showToast } from "../ToastNotification/ToastNotification";
import "./Login.scss";

function Login({ isOpen, onClose, switchToRegister }) {
  const [formData, setFormData] = useState({
    email: "",
    password: ""
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password) {
      showToast("Please enter both email and password!", "error");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/auth/login/", {
        email: formData.email,
        password: formData.password
      });

      showToast("Login successful!", "success");

      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);

      // TODO: Add user redirect after login
    } catch (err) {
      showToast(err.response?.data?.message || "Invalid credentials", "error");
    }
  };

  if (!isOpen) return null;

  return (
    <div className="login-overlay" onClick={onClose}>
      <div className="login-popup" onClick={(e) => e.stopPropagation()}>
        <h2>Login</h2>

        <form onSubmit={handleSubmit}>
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
            placeholder="Enter your password"
            required
            value={formData.password}
            onChange={handleChange}
          />

          <p className="forgot-password">Forgot Password?</p>

          <button type="submit" className="login-btn">Login</button>
        </form>

        <p className="register-link">
          Don't have an account? <span onClick={switchToRegister}>Register</span>
        </p>

        <button className="close-btn" onClick={onClose}>&times;</button>
      </div>
    </div>
  );
}

export default Login;
