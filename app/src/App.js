import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ProtectedRoute, RedirectHome } from './middleware';
import { GoTop, Footer, ToastNotification, Admin, Company, Employee, Unauthorized, NotFound, EmployeeManagement, UserManagement, ResetPassword, Quizzes, EmployeeQuizzes, EmployeeQuizDetail, QuizTaking, EmployeeProfile } from './components';
import './App.scss';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<RedirectHome />} />
        <Route path="/reset-password/:uidb64/:token" element={<ResetPassword />} />

        <Route path="/admin" element={<ProtectedRoute allowedRoles={["admin"]}><Admin /></ProtectedRoute>} />
        <Route path="/admin/users-management" element={<ProtectedRoute allowedRoles={["admin"]}><UserManagement /></ProtectedRoute>} />

        <Route path="/company" element={<ProtectedRoute allowedRoles={["company"]}><Company /></ProtectedRoute>} />
        <Route path="/company/employees-management" element={<ProtectedRoute allowedRoles={["company"]}><EmployeeManagement /></ProtectedRoute>} />
        <Route path="/company/quizzes" element={<ProtectedRoute allowedRoles={["company"]}><Quizzes /></ProtectedRoute>} />

        <Route path="/employee" element={<ProtectedRoute allowedRoles={["employee"]}><Employee /></ProtectedRoute>} />
        <Route path="/employee/quizzes" element={<ProtectedRoute allowedRoles={["employee"]} ><EmployeeQuizzes /></ProtectedRoute>} />
        <Route path="/employee/quiz/:id" element={<ProtectedRoute allowedRoles={["employee"]}><EmployeeQuizDetail /></ProtectedRoute>} />
        <Route path="/employee/quiz/:id/take" element={<ProtectedRoute allowedRoles={["employee"]}><QuizTaking /></ProtectedRoute>} />
        <Route path="/employee/profile" element={<ProtectedRoute allowedRoles={["employee"]}><EmployeeProfile /></ProtectedRoute>} />

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
