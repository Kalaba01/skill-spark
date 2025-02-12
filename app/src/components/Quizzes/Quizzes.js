import React, { useState, useEffect } from "react";
import { TopBar, QuizForm, ConfirmPopup, QuizCard } from "../";
import { useTranslation } from "react-i18next";
import { showToast } from "../ToastNotification/ToastNotification";
import axios from "axios";
import "./Quizzes.scss";

function Quizzes() {
  const { t } = useTranslation();
  const [quizzes, setQuizzes] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [difficultyFilter, setDifficultyFilter] = useState("");
  const [confirmDelete, setConfirmDelete] = useState({ isOpen: false, quizId: null });

  const fetchQuizzes = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(
        "http://127.0.0.1:8000/api/quizzes/",
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setQuizzes(response.data);
    } catch (error) {
      showToast(t("quizzes.load_error"), "error");
    }
  };

  useEffect(() => {
    fetchQuizzes();
  }, []);

  const handleEdit = (quiz) => {
    setSelectedQuiz(quiz);
    setIsFormOpen(true);
  };

  const handleDeleteClick = (quizId) => {
    setConfirmDelete({ isOpen: true, quizId });
  };

  const handleConfirmDelete = async () => {
    if (!confirmDelete.quizId) return;

    try {
      const token = localStorage.getItem("access_token");
      await axios.delete(
        `http://127.0.0.1:8000/api/quizzes/${confirmDelete.quizId}/`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      showToast(t("quizzes.delete_success"), "success");
      fetchQuizzes();
    } catch (error) {
      showToast(t("quizzes.delete_error"), "error");
    } finally {
      setConfirmDelete({ isOpen: false, quizId: null });
    }
  };

  const filteredQuizzes = quizzes.filter((quiz) => {
    return (
      quiz.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
      (difficultyFilter === "" || quiz.difficulty === difficultyFilter)
    );
  });

  return (
    <>
      <TopBar />
      <div className="quizzes">
        <h2>{t("quizzes.your_quizzes")}</h2>

        <div className="toolbar">
          <input
            type="text"
            placeholder={t("quizzes.search_placeholder")}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <select
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
          >
            <option value="">{t("quizzes.filter_label")}</option>
            <option value="easy">{t("quizzes.difficulty_easy")}</option>
            <option value="medium">{t("quizzes.difficulty_medium")}</option>
            <option value="hard">{t("quizzes.difficulty_hard")}</option>
          </select>
          <button className="add-quiz-btn" onClick={() => setIsFormOpen(true)}>
            {t("quizzes.add_quiz")}
          </button>
        </div>

        <div className="quiz-cards">
          {filteredQuizzes.length > 0 ? (
            filteredQuizzes.map((quiz) => (
              <QuizCard
                key={quiz.id}
                quiz={quiz}
                actions={
                  <div className="actions">
                    <button className="edit-btn" onClick={() => handleEdit(quiz)}>
                      {t("quizzes.edit")}
                    </button>
                    <button className="delete-btn" onClick={() => handleDeleteClick(quiz.id)}>
                      {t("quizzes.delete")}
                    </button>
                  </div>
                }
              />
            ))
          ) : (
            <p className="no-quizzes">
              {searchTerm || difficultyFilter
                ? t("quizzes.no_quizzes_found")
                : t("quizzes.no_quizzes")}
            </p>
          )}
        </div>

        {isFormOpen && (
          <QuizForm
            quiz={selectedQuiz}
            onClose={() => {
              setIsFormOpen(false);
              setSelectedQuiz(null);
              fetchQuizzes();
            }}
          />
        )}

        {confirmDelete.isOpen && (
          <ConfirmPopup
            message={t("quizzes.delete_message")}
            onConfirm={handleConfirmDelete}
            onCancel={() => setConfirmDelete({ isOpen: false, quizId: null })}
          />
        )}
      </div>
    </>
  );
}

export default Quizzes;
