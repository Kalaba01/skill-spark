import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { LandingPage, GoTop, Footer, ToastNotification } from './components';
import { Provider } from "react-redux";
import store from "./store";
import './App.css';

function App() {
  return (
    <>
    <Provider store={store}>
      <Routes>
        <Route path="/" element={<LandingPage />} />
      </Routes>
      
      <ToastNotification />
      <GoTop />
      <Footer />
    </Provider>
    </>
  );
}

export default App;
