import { createSlice } from "@reduxjs/toolkit";

// Retrieves the stored language from localStorage or defaults to "en" (English)
const storedLanguage = localStorage.getItem("language") || "en";

/**
 * Redux slice for managing the application's language state.
 * - Persists language preference in localStorage.
 * - Allows users to dynamically switch between languages.
 */

const languageSlice = createSlice({
  name: "language",
  initialState: { language: storedLanguage },
  reducers: {
    // Updates the language state and stores the new language in localStorage
    setLanguage: (state, action) => {
      state.language = action.payload;
      localStorage.setItem("language", action.payload);
    }
  }
});

export const { setLanguage } = languageSlice.actions;
export default languageSlice.reducer;
