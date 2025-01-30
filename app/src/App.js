import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { LandingPage } from './components';
import './App.css';

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
    </Routes>
  );
}

export default App;
