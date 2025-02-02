import React from "react";
import { FaSun, FaMoon } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { toggleTheme } from "../../store/themeSlice";

function Theme() {
    const dispatch = useDispatch();
    const theme = useSelector((state) => state.theme.theme);

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
