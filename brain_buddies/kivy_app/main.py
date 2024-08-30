import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class BrainBuddiesApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Initial Welcome Label
        self.label = Label(text="Welcome to Brain Buddies, [User's Name]!")
        self.layout.add_widget(self.label)

        # Math Challenge Button
        self.math_button = Button(text="Start Math Challenge")
        self.math_button.bind(on_press=self.start_math_challenge)
        self.layout.add_widget(self.math_button)

        # Science Challenge Button
        self.science_button = Button(text="Start Science Challenge")
        self.science_button.bind(on_press=self.start_science_challenge)
        self.layout.add_widget(self.science_button)

        # Answer Input (initially hidden)
        self.answer_input = TextInput(hint_text="Enter your answer here", multiline=False)
        self.answer_input.bind(on_text_validate=self.check_answer)

        # Score Label (initially hidden)
        self.score_label = Label(text="Score: 0")

        # Initialize state
        self.score = 0
        self.current_question_index = 0
        self.questions = []

        return self.layout
    
    def start_math_challenge(self, instance):
        # Update the screen for the math challenge
        self.label.text = "Math Challenge Started!"
        self.clear_buttons()
        self.layout.add_widget(self.answer_input)
        self.layout.add_widget(self.score_label)
        self.fetch_questions('math')

    def start_science_challenge(self, instance):
        # Update the screen for the science challenge
        self.label.text = "Science Challenge Started!"
        self.clear_buttons()
        self.layout.add_widget(self.answer_input)
        self.layout.add_widget(self.score_label)
        self.fetch_questions('science')

    def clear_buttons(self):
        self.layout.remove_widget(self.math_button)
        self.layout.remove_widget(self.science_button)
    
    def fetch_questions(self, challenge_type):
        # Fetch questions from the Django API
        try:
            response = requests.get(f'http://127.0.0.1:8000/api/{challenge_type}_challenges')
            response.raise_for_status()
            self.questions = response.json()
        except requests.exceptions.RequestException as e:
            self.label.text = f"Error fetching challenges: {str(e)}"
            self.questions = []
            return

        if self.questions:
            self.display_question()
        else:
            self.label.text = "No challenges available!"

    def display_question(self):
        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            self.label.text = current_question["question"]
            self.answer_input.bind(on_text_validate=self.check_answer)
        else:
            self.label.text = "No more questions available!"
            self.end_challenge()

    def check_answer(self, instance):
        try:
            user_answer = self.answer_input.text.strip().lower()
            current_question = self.questions[self.current_question_index]

            if user_answer == current_question["answer"].strip().lower():
                self.label.text = "Correct!"
                self.score += current_question["points"]
            else:
                self.label.text = "Try again!"
        
            self.score_label.text = f"Score: {self.score}"
            self.answer_input.text = ""

            self.current_question_index += 1

            if self.current_question_index < len(self.questions):
                self.display_question()
            else:
                self.label.text = "Challenge Complete!"
                self.end_challenge()
        except Exception as e:
                self.label.text = f"Error: {str(e)}"

    def end_challenge(self):
        self.answer_input.unbind(on_text_validate=self.check_answer)
        self.layout.remove_widget(self.answer_input)
        self.layout.remove_widget(self.score_label)

if __name__ == "__main__":
    BrainBuddiesApp().run()