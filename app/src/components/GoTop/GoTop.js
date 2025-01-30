import React, { useState, useEffect } from 'react';
import './GoTop.scss';
import { FaArrowUp } from 'react-icons/fa';

function GoTop() {
  const [isVisible, setIsVisible] = useState(false);

  // Funkcija koja proverava koliko je korisnik skrolovao
  const toggleVisibility = () => {
    if (window.scrollY > 300) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    }
  };

  // Funkcija za povratak na vrh
  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  // Praćenje skrolovanja
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
