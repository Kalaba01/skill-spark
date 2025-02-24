import React, { useState, useEffect } from 'react';
import { FaArrowUp } from 'react-icons/fa';
import './GoTop.scss';

function GoTop() {
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => {
    if (window.scrollY > 300) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

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
