import React from "react";
import { FaSun, FaMoon } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { toggleTheme } from "../../store/themeSlice";

/**
 * Theme Component
 *
 * - Allows users to toggle between light and dark themes.
 * - Uses Redux state to track the current theme.
 * - Dispatches an action to update the theme in Redux store when clicked.
 */

function Theme() {
    const dispatch = useDispatch();
    const theme = useSelector((state) => state.theme.theme); // Fetches current theme from Redux store

    return(
        <>
        {theme === "light" ? (
            <FaMoon size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
            ) : (
            <FaSun size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
        )}
        </>
    )
}

export default Theme;
