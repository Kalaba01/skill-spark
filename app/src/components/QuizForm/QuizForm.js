import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { QuestionForm } from "../";
import { showToast } from "../ToastNotification/ToastNotification";
import axios from "axios";
import "./QuizForm.scss";

/**
 * QuizForm Component
 * - Allows users to create or edit a quiz.
 * - Supports adding, editing, and removing questions.
 * - Includes form validation and API calls for quiz creation/update.
 */

function QuizForm({ quiz, onClose }) {
  const { t } = useTranslation();

  const [formData, setFormData] = useState({
    title: quiz?.title || "",
    description: quiz?.description || "",
    difficulty: quiz?.difficulty || "easy",
    duration: quiz?.duration || 30,
    questions: quiz?.questions || [],
  });

  const [isQuestionFormOpen, setIsQuestionFormOpen] = useState(false);
  const [editingQuestionIndex, setEditingQuestionIndex] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Adds or updates a question in the quiz
  const handleAddQuestion = (question) => {
    let updatedQuestions = [...formData.questions];

    if (editingQuestionIndex !== null) {
      updatedQuestions[editingQuestionIndex] = question;
    } else {
      updatedQuestions.push(question);
    }

    setFormData({ ...formData, questions: updatedQuestions });
    setEditingQuestionIndex(null);
    setIsQuestionFormOpen(false);
  };

  // Opens question editor for an existing question
  const handleEditQuestion = (index) => {
    setEditingQuestionIndex(index);
    setIsQuestionFormOpen(true);
  };

  // Deletes a question from the quiz
  const handleDeleteQuestion = (index) => {
    const updatedQuestions = formData.questions.filter((_, i) => i !== index);
    setFormData({ ...formData, questions: updatedQuestions });
  };

  // Truncates long text for display
  const truncateText = (text, maxLength) => {
    return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
  };

  // Submits the quiz
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("access_token");

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      };

      if (quiz) {
        await axios.put(
          `http://127.0.0.1:8000/api/quizzes/${quiz.id}/`,
          formData,
          config
        );
        showToast(t("quiz_form.update_success"), "success");
      } else {
        await axios.post(
          "http://127.0.0.1:8000/api/quizzes/",
          formData,
          config
        );
        showToast(t("quiz_form.create_success"), "success");
      }
      onClose();
    } catch (error) {
      console.error("Error sending data:", error.response?.data || error);
      showToast(t("quiz_form.save_error"), "error");
    }
  };

  return (
    <div className="quiz-form-overlay" onClick={onClose}>
      <div className="quiz-form-popup" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>
          &times;
        </button>
        <h2>{quiz ? t("quiz_form.edit_quiz") : t("quiz_form.create_quiz")}</h2>
        <form onSubmit={handleSubmit}>
          <label>{t("quiz_form.title")}</label>
          <input type="text" name="title" value={formData.title} onChange={handleChange} required />

          <label>{t("quiz_form.description")}</label>
          <textarea name="description" value={formData.description} onChange={handleChange} required />

          <div className="form-row">
            <div className="form-group">
              <label>{t("quiz_form.difficulty")}</label>
              <select name="difficulty" value={formData.difficulty} onChange={handleChange}>
                <option value="easy">{t("quiz_form.difficulty_easy")}</option>
                <option value="medium">{t("quiz_form.difficulty_medium")}</option>
                <option value="hard">{t("quiz_form.difficulty_hard")}</option>
              </select>
            </div>

            <div className="form-group">
              <label>{t("quiz_form.duration")}</label>
              <input type="number" name="duration" value={formData.duration} onChange={handleChange} min="1" required />
            </div>
          </div>

          <div className="questions">
            <h3>{t("quiz_form.questions")}</h3>
            <div className="questions-list">
              {formData.questions.map((question, index) => (
                <div key={index} className="question-card">
                  <p className="question-text">{truncateText(question.text, 50)}</p>
                  <ul className="answer-list">
                    {question.answers.map((answer, i) => (
                      <li key={i} className={answer.is_correct ? "correct" : ""}>
                        {truncateText(answer.text, 30)}
                      </li>
                    ))}
                  </ul>
                  <div className="question-actions">
                    <button type="button" className="edit-btn" onClick={() => handleEditQuestion(index)}>
                      {t("quiz_form.edit")}
                    </button>
                    <button type="button" className="delete-btn" onClick={() => handleDeleteQuestion(index)}>
                      {t("quiz_form.delete")}
                    </button>
                  </div>
                </div>
              ))}
            </div>
            <button
              type="button"
              onClick={() => {
                setEditingQuestionIndex(null);
                setIsQuestionFormOpen(true);
              }}
            >
              {t("quiz_form.add_question")}
            </button>
          </div>

          <button type="submit">{quiz ? t("quiz_form.update_quiz") : t("quiz_form.create_quiz")}</button>
        </form>
      </div>

      {/* Question Form Popup */}
      {isQuestionFormOpen && (
        <QuestionForm
          onClose={() => setIsQuestionFormOpen(false)}
          onSave={handleAddQuestion}
          initialData={editingQuestionIndex !== null ? formData.questions[editingQuestionIndex] : { text: "", answers: [{ text: "", is_correct: false }] }}
        />
      )}
    </div>
  );
}

export default QuizForm;
