import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import "./QuestionForm.scss";

/**
 * QuestionForm Component
 *
 * - Allows users to create or edit a quiz question.
 * - Supports multiple answers with the ability to mark correct ones.
 * - Provides form validation to ensure all fields are filled.
 */

function QuestionForm({ onClose, onSave, initialData }) {
  const { t } = useTranslation();
  
  const [question, setQuestion] = useState(
    initialData || { text: "", answers: [{ text: "", is_correct: false }] }
  );

  // Handles question text change
  const handleQuestionChange = (e) => {
    setQuestion({ ...question, text: e.target.value });
  };

  // Handles answer text change
  const handleAnswerChange = (index, value) => {
    const updatedAnswers = [...question.answers];
    updatedAnswers[index].text = value;
    setQuestion({ ...question, answers: updatedAnswers });
  };

  // Toggles the correct answer selection
  const handleCorrectAnswerToggle = (index) => {
    const updatedAnswers = [...question.answers];
    updatedAnswers[index].is_correct = !updatedAnswers[index].is_correct;
    setQuestion({ ...question, answers: updatedAnswers });
  };

  // Adds a new answer field
  const addAnswer = () => {
    setQuestion({
      ...question,
      answers: [...question.answers, { text: "", is_correct: false }],
    });
  };

  // Removes an answer field
  const removeAnswer = (index) => {
    const updatedAnswers = question.answers.filter((_, i) => i !== index);
    setQuestion({ ...question, answers: updatedAnswers });
  };

  // Validates input and saves the question
  const handleSave = () => {
    if (question.text.trim() === "" || question.answers.some((a) => a.text.trim() === "")) {
      alert(t("question_form.fill_all_fields"));
      return;
    }
    onSave(question);
    onClose();
  };

  return (
    <div className="question-form-overlay" onClick={onClose}>
      <div className="question-form-popup" onClick={(e) => e.stopPropagation()}>
        <h2>{initialData ? t("question_form.edit_question") : t("question_form.add_question")}</h2>

        <label>{t("question_form.question_text")}</label>
        <input
          type="text"
          placeholder={t("question_form.enter_question")}
          value={question.text}
          onChange={handleQuestionChange}
        />

        <h3>{t("question_form.answers")}</h3>
        {question.answers.map((answer, index) => (
          <div key={index} className="answer-row">
            <input
              type="text"
              placeholder={t("question_form.answer_text")}
              value={answer.text}
              onChange={(e) => handleAnswerChange(index, e.target.value)}
            />
            <input
              type="checkbox"
              checked={answer.is_correct}
              onChange={() => handleCorrectAnswerToggle(index)}
            />
            <button className="remove-btn" onClick={() => removeAnswer(index)}>✖</button>
          </div>
        ))}

        <button className="add-answer-btn" onClick={addAnswer}>{t("question_form.add_answer")}</button>
        <div className="question-form-actions">
          <button className="save-btn" onClick={handleSave}>{t("question_form.save_question")}</button>
          <button className="cancel-btn" onClick={onClose}>{t("question_form.cancel")}</button>
        </div>
      </div>
    </div>
  );
}

export default QuestionForm;
