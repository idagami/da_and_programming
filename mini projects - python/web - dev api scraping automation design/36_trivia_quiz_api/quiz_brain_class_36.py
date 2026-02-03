import html


class QuizBrain:
    def __init__(self, questions_list):
        self.question_number = 0
        self.question_list = questions_list
        self.score = 0

    def still_has_questions(self):
        return self.question_number < len(self.question_list)  # returns True or False

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        q_text = html.unescape(self.current_question.text)
        self.question_number += 1
        return f"Q.{self.question_number} {q_text} (True / False): "

    def check_answer(self, user_input):
        correct_answer = self.current_question.answer
        if user_input == correct_answer:
            self.score += 1
            return True
        else:
            return False
