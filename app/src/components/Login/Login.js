import React from "react";
import "./Login.scss";

function Login({ isOpen, onClose, switchToRegister }) {
  if (!isOpen) return null;

  return (
    <div className="login-overlay" onClick={onClose}>
      <div className="login-popup" onClick={(e) => e.stopPropagation()}>
        <h2>Login</h2>
        <form>
          <label>Email</label>
          <input type="email" placeholder="Enter your email" required />

          <label>Password</label>
          <input type="password" placeholder="Enter your password" required />

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
