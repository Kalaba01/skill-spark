import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { TopBar, Loading } from "../";
import { useTranslation } from "react-i18next";
import axios from "axios";
import "./QuizTaking.scss";

const QuizTaking = () => {
  const { t } = useTranslation();
  const { id } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(null);
  const [result, setResult] = useState(null);

  const shuffleArray = (array) => {
    return array.sort(() => Math.random() - 0.5);
  };

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get(
          `http://127.0.0.1:8000/api/quizzes/${id}/take/`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const shuffledQuiz = {
          ...response.data,
          questions: response.data.questions.map((question) => ({
            ...question,
            answers: shuffleArray([...question.answers]),
          })),
        };

        setQuiz(shuffledQuiz);
        setTimeLeft(response.data.duration * 60);
      } catch (error) {
        if (error.response && error.response.status === 403) {
          navigate("/unauthorized");
        } else {
          console.error("Error fetching quiz data:", error);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchQuiz();
  }, [id, navigate]);

  useEffect(() => {
    if (timeLeft === null || result) return;

    if (timeLeft <= 0) {
      handleSubmit();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prevTime) => prevTime - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  const handleAnswerChange = (questionId, answerId) => {
    setAnswers((prev) => {
      const selected = prev[questionId] || [];
      if (selected.includes(answerId)) {
        return { ...prev, [questionId]: selected.filter((id) => id !== answerId) };
      } else {
        return { ...prev, [questionId]: [...selected, answerId] };
      }
    });
  };

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.post(
        `http://127.0.0.1:8000/api/quizzes/${id}/take/`,
        answers,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(response.data);
      setTimeLeft(null);
    } catch (error) {
      console.error("Error submitting quiz:", error);
    }
  };

  const getTimerClass = () => {
    if (timeLeft === null) return "timer blue";
    if (timeLeft <= 60) return "timer red";
    if (timeLeft <= 120) return "timer yellow";
    return "timer blue";
  };

  if (loading) {
    return (
      <>
        <TopBar />
        <Loading />
      </>
    );
  }

  if (!quiz) {
    return null;
  }

  return (
    <>
      <TopBar />
      <div className="quiz-taking-container">
        <h1>{quiz.title}</h1>
        <div className={getTimerClass()}>
          {t("quiz_taking.time_left")}: {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, "0")}
        </div>

        {result ? (
          <div className="result">
            <h2>{t("quiz_taking.result")}</h2>
            <p>
              {t("quiz_taking.correct_answers")}: {result.correct_answers} / {result.total_questions}
            </p>
            <button onClick={() => navigate("/employee")}>{t("quiz_taking.return_dashboard")}</button>
          </div>
        ) : (
          <>
            <div className="questions">
              {quiz.questions.map((question) => (
                <div key={question.id} className="question">
                  <h3>{question.text}</h3>
                  <div className="answers">
                    {question.answers.map((answer) => (
                      <label key={answer.id} className="answer-option">
                        <input
                          type="checkbox"
                          checked={answers[question.id]?.includes(answer.id) || false}
                          onChange={() => handleAnswerChange(question.id, answer.id)}
                        />
                        {answer.text}
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <button onClick={handleSubmit} className="submit-btn">
              {t("quiz_taking.submit")}
            </button>
          </>
        )}
      </div>
    </>
  );
};

export default QuizTaking;
