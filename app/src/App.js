import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { LandingPage, GoTop, Footer, ToastNotification, Admin, Company } from './components';
import './App.css';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/company" element={<Company />} />
      </Routes>
      
      <ToastNotification />
      <GoTop />
      <Footer />
    </>
  );
}

export default App;
