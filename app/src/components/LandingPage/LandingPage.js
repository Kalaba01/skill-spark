import React, { useState } from "react";
import "./LandingPage.scss";
import { FaUserCircle, FaSun, FaMoon, FaGlobe, FaChevronDown } from "react-icons/fa";
import { Login, Register } from "../index";
import { useDispatch, useSelector } from "react-redux";
import { toggleTheme } from "../../store/themeSlice";

function LandingPage() {
  const [faqOpen, setFaqOpen] = useState(null);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [isRegisterOpen, setIsRegisterOpen] = useState(false);

  const dispatch = useDispatch();
  const theme = useSelector((state) => state.theme.theme);

  const toggleFaq = (index) => {
    setFaqOpen(faqOpen === index ? null : index);
  };

  const openLogin = () => {
    setIsRegisterOpen(false);
    setIsLoginOpen(true);
  };

  const openRegister = () => {
    setIsLoginOpen(false);
    setIsRegisterOpen(true);
  };

  return (
    <div className="landing-page">
      {/* Top Bar */}
      <header className="top-bar">
        <div className="logo">SkillSpark</div>
        <div className="top-bar-icons">
          <FaUserCircle size={24} className="icon" onClick={openLogin} />
          {theme === "light" ? (
            <FaMoon size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
          ) : (
            <FaSun size={24} className="icon" onClick={() => dispatch(toggleTheme())} />
          )}
          <FaGlobe size={24} className="icon" />
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <h1>Revolutionize Employee Training</h1>
      </section>

      {/* Features Section */}
      <section id="features" className="features">
        <h2>Why Choose SkillSpark?</h2>

        <div className="feature-item">
          <img src="https://placehold.co/600x400" alt="Feature 1" />
          <div>
            <h3>Engaging and Interactive Quizzes</h3>
            <p>
              Traditional training methods often struggle to maintain employee
              engagement, leading to lower knowledge retention. SkillSpark
              transforms corporate training with interactive quizzes that make
              learning more dynamic and effective. By integrating gamification,
              employees stay motivated, improving participation and
              comprehension. Our quizzes adapt to each employee's learning pace,
              providing personalized challenges based on performance. Instant
              feedback helps reinforce knowledge, ensuring employees grasp key
              concepts in real-time. The platform is accessible across multiple
              devices, allowing employees to complete training at their
              convenience, whether in the office or working remotely. This
              flexibility makes training more efficient and less disruptive.
            </p>
          </div>
        </div>

        <div className="feature-item reverse">
          <img src="https://placehold.co/600x400" alt="Feature 2" />
          <div>
            <h3>Data-Driven Training with Advanced Analytics</h3>
            <p>
              SkillSpark’s advanced analytics give businesses real-time insights
              into employee progress, helping managers track training
              effectiveness and identify areas for improvement. Companies can
              monitor quiz completion rates and scores to detect employees who
              may need additional support. By analyzing performance trends,
              managers can refine training programs to focus on the most
              relevant skill gaps. SkillSpark also offers customizable reporting
              dashboards, making it easy for HR and leadership teams to generate
              meaningful insights. These reports empower businesses to optimize
              training strategies, ensuring measurable growth and alignment with
              organizational goals.
            </p>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="faq">
        <h2>Frequently Asked Questions</h2>
        {[
          {
            question: "What is SkillSpark?",
            answer:
              "SkillSpark is a corporate training platform that enables businesses to create, manage, and track employee training through interactive quizzes. It helps companies improve knowledge retention, boost engagement, and measure learning outcomes effectively.",
          },
          {
            question: "How does SkillSpark improve employee learning?",
            answer:
              "SkillSpark provides a structured learning path through quizzes tailored to each employee’s needs. Our real-time analytics highlight strengths and weaknesses, allowing managers to address knowledge gaps effectively. The platform also supports adaptive learning, where questions adjust in difficulty based on employee performance.",
          },
          {
            question: "Can SkillSpark integrate with our existing HR or LMS systems?",
            answer:
              "Absolutely! SkillSpark is designed to integrate with popular HR and LMS systems, ensuring seamless synchronization of employee progress, training modules, and certification tracking. Our API allows businesses to automate training workflows effortlessly.",
          }
        ].map((faq, index) => (
          <div
            key={index}
            className={`faq-item ${faqOpen === index ? "open" : ""}`}
            onClick={() => toggleFaq(index)}
          >
            <div className="faq-header">
              <h3>{faq.question}</h3>
              <FaChevronDown
                className={`arrow ${faqOpen === index ? "rotate" : ""}`}
              />
            </div>
            <div className="faq-answer">
              {faqOpen === index && <p>{faq.answer}</p>}
            </div>
          </div>
        ))}
      </section>

      {/* Login and Register Popups */}
      <Login isOpen={isLoginOpen} onClose={() => setIsLoginOpen(false)} switchToRegister={openRegister} />
      <Register isOpen={isRegisterOpen} onClose={() => setIsRegisterOpen(false)} switchToLogin={openLogin} />

    </div>
  );
}

export default LandingPage;
