import React from "react";
import "./Register.scss";

function Register({ isOpen, onClose, switchToLogin }) {
  if (!isOpen) return null;

  return (
    <div className="register-overlay" onClick={onClose}>
      <div className="register-popup" onClick={(e) => e.stopPropagation()}>
        <h2>Register</h2>
        <form>
          <label>Company Name</label>
          <input type="text" placeholder="Enter company name" required />

          <label>Email</label>
          <input type="email" placeholder="Enter your email" required />

          <label>Password</label>
          <input type="password" placeholder="Create a password" required />

          <label>Confirm Password</label>
          <input type="password" placeholder="Confirm your password" required />

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
