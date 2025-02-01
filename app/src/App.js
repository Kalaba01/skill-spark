import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { LandingPage, GoTop, Footer, ToastNotification, Admin } from './components';
import './App.css';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
      
      <ToastNotification />
      <GoTop />
      <Footer />
    </>
  );
}

export default App;
