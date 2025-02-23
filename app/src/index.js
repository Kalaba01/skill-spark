import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import { Provider } from "react-redux";
import App from './App';
import store from './store';
import './index.scss';
import "./i18n";

/**
 * Root file of the React application.
 * - Wraps the app with Redux Provider for state management.
 * - Uses React Router for navigation.
 * - Loads global styles and i18n for internationalization.
 */

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <Router>
        <App />
      </Router>
    </Provider>
  </React.StrictMode>
);
