from question_model_36 import Question
from data import question_data
from quiz_brain_class_36 import QuizBrain
from ui_36 import QuizInterface

question_bank = []
for question in question_data:
    q_text = question["question"]
    q_answer = question["correct_answer"]
    new_q = Question(q_text, q_answer)
    question_bank.append(new_q)

quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface(quiz)

# while quiz.still_has_questions(): # commented as we have mainloop in UI class. Otherwise wont work
#     quiz.next_question()
