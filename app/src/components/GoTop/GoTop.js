import React, { useState, useEffect } from 'react';
import { FaArrowUp } from 'react-icons/fa';
import './GoTop.scss';

/**
 * GoTop Component
 *
 * - Displays a scroll-to-top button when the user scrolls down.
 * - Clicking the button smoothly scrolls the page back to the top.
 * - Listens for scroll events to determine visibility.
 */

function GoTop() {
  const [isVisible, setIsVisible] = useState(false);

  // Toggles button visibility based on scroll position
  const toggleVisibility = () => {
    if (window.scrollY > 300) { // Becomes visible when the user scrolls past 300px
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  };

  // Smoothly scrolls the page to the top when clicked
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  // Adds a scroll event listener on mount and removes it on unmount
  useEffect(() => {
    window.addEventListener('scroll', toggleVisibility);
    return () => window.removeEventListener('scroll', toggleVisibility);
  }, []);

  return (
    <div className={`go-top ${isVisible ? 'visible' : ''}`} onClick={scrollToTop}>
      <FaArrowUp className="arrow-icon" />
    </div>
  );
}

export default GoTop;
