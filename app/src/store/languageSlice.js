import { createSlice } from "@reduxjs/toolkit";

const storedLanguage = localStorage.getItem("language") || "en";

const languageSlice = createSlice({
  name: "language",
  initialState: { language: storedLanguage },
  reducers: {
    setLanguage: (state, action) => {
      state.language = action.payload;
      localStorage.setItem("language", action.payload);
    },
  },
});

export const { setLanguage } = languageSlice.actions;
export default languageSlice.reducer;
