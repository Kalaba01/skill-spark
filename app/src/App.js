import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { LandingPage, GoTop } from './components';
import './App.css';

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage />} />
      </Routes>
      <GoTop />
    </>
  );
}

export default App;
