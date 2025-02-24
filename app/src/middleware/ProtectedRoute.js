import React from "react";
import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

/**
 * ProtectedRoute middleware
 * - Restricts access to specific routes based on user roles.
 * - Checks if the user is authenticated via a JWT token.
 * - Redirects unauthorized users to the appropriate pages.
 */

const ProtectedRoute = ({ allowedRoles, children }) => {
  const token = localStorage.getItem("access_token");

  // Redirect to home if no token is found
  if (!token) {
    return <Navigate to="/" replace />;
  }

  try {
    const decodedToken = jwtDecode(token);

    // Check if the token is expired
    const currentTime = Date.now() / 1000;
    if (decodedToken.exp < currentTime) {
      localStorage.removeItem("access_token"); // Clear expired token
      return <Navigate to="/" replace />;
    }

    // Check if the user's role is allowed to access the route
    if (!allowedRoles.includes(decodedToken.user.role)) {
      return <Navigate to="/unauthorized" replace />;
    }

    // If all checks pass, render the protected content
    return children;
  } catch (error) {
    console.error("Invalid token:", error);
    return <Navigate to="/" replace />;
  }
};

export default ProtectedRoute;
