import { createSlice } from "@reduxjs/toolkit";

// Retrieves the stored theme from localStorage or defaults to "light"
const storedTheme = localStorage.getItem("theme") || "light";

// Apply the theme to the document body
document.body.classList.toggle("dark-mode", storedTheme === "dark");

/**
 * Redux slice for managing the application's theme (light/dark mode).
 *
 * - Persists theme preference in localStorage.
 * - Dynamically toggles between "light" and "dark" themes.
 * - Applies the selected theme to the document body.
 */

const themeSlice = createSlice({
  name: "theme",
  initialState: {
    theme: storedTheme
  },
  reducers: {
    // Toggles between light and dark themes and updates localStorage and applies the theme globally
    toggleTheme: (state) => {
      state.theme = state.theme === "light" ? "dark" : "light";
      localStorage.setItem("theme", state.theme);
      document.body.classList.toggle("dark-mode", state.theme === "dark");
    }
  }
});

// Export actions and reducer
export const { toggleTheme } = themeSlice.actions;
export default themeSlice.reducer;
