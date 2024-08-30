import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class BrainBuddiesApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Initial Welcome Label
        self.label = Label(text="Welcome to Brain Buddies, [User's Name]!")
        layout.add_widget(self.label)

        # Math Challenge Button
        math_button = Button(text="Start Math Challenge")
        math_button.bind(on_press=self.start_math_challenge)
        layout.add_widget(math_button)

        # Science Challenge Button
        science_button = Button(text="Start Science Challenge")
        science_button.bind(on_press=self.start_science_challenge)
        layout.add_widget(science_button)

        # Score Label (initially hidden)
        self.score_label = Label(text="Score: 0")
        self.score_label.opacity = 0
        layout.add_widget(self.score_label)

        # Answer Input (initially hidden)
        self.answer_input = TextInput(hint_text="Enter your answer here", multiline=False)
        self.answer_input.opacity = 0
        layout.add_widget(self.answer_input)

        # Initialize state
        self.score = 0
        self.current_question_index = 0
        self.question = []

        return layout
    
    def start_math_challenge(self, instance):
        # Update the screen for the math challenge
        self.label.text = "Math Challenge Started!"
        self.show_challenge_ui()
        self.fetch_questions('math')

    def start_science_challenge(self, instance):
        # Update the screen for the science challenge
        self.label.text = "Science Challenge Started!"
        self.show_challenge_ui()
        self.fetch_questions('science')
    
    def fetch_questions(self, challenge_type):
        # Fetch questions from the Django API
        try:
            response = requests.get(f'http://127.0.0.1:8000/api/{challenge_type}_challenges/')
            response.raise_for_status()
            self.questions = response.json()
        except requests.exceptions.RequestException as e:
            self.label.text = f"Error fetching challenges: {str(e)}"
            self.questions = []

        if self.questions:
            self.display_question()
        else:
            self.label.text = "No challenges available!"

    def display_question(self):
        # Display the first question and prepare for user input
        current_question = self.questions[self.current_question_index]
        self.label.text = current_question["question"]
        self.answer_input.text = ""
        self.answer_input.bind(on_text_validate=self.check_answer)

    def check_answer(self, instance):
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
            self.answer_input.unbind(on_text_validate=self.check_answer)
    
    def show_challenge_ui(self):
        # Show the input field and score label when a challenge starts
        self.score_label.opacity = 1
        self.answer_input.opacity = 1
        self.answer_input.focus = True

if __name__ == "__main__":
    BrainBuddiesApp().run()