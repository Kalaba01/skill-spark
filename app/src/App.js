import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ProtectedRoute, RedirectHome } from './middleware';
import { GoTop, Footer, ToastNotification, Admin, Company, Employee, Unauthorized, NotFound, EmployeeManagement, UserManagement } from './components';
import './App.css';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<RedirectHome />} />

        <Route path="/admin" element={<ProtectedRoute allowedRoles={["admin"]}><Admin /></ProtectedRoute>} />
        <Route path="/admin/users-management" element={<ProtectedRoute allowedRoles={["admin"]}><UserManagement /></ProtectedRoute>} />

        <Route path="/company" element={<ProtectedRoute allowedRoles={["company"]}><Company /></ProtectedRoute>} />
        <Route path="/company/employees-management" element={<ProtectedRoute allowedRoles={["company"]}><EmployeeManagement /></ProtectedRoute>} />

        <Route path="/employee" element={<ProtectedRoute allowedRoles={["employee"]}><Employee /></ProtectedRoute>} />

        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route path="*" element={<NotFound />} />

      </Routes>
      
      <ToastNotification />
      <GoTop />
      <Footer />
    </>
  );
}

export default App;
