import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

# Screen for user sign-in
class SignInScreen(Screen):
    def __init__(self, **kwargs):
        super(SignInScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input =TextInput(hint_text='Password', multiline=False, password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        sign_in_button = Button(text="Sign In")
        sign_in_button.bind(on_press=self.sign_in)
        layout.add_widget(sign_in_button)

        sign_up_button = Button(text="Sign Up")
        sign_up_button.bind(on_press=self.go_to_sign_up)
        layout.add_widget(sign_up_button)

        self.add_widget(layout)

    def sign_in(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username == 'test' and password == "password":
            self.manager.current = 'main'
            self.manager.get_screen('main').label.text = f"Welcome to Brain Buddies, {username}!"
        else:
            self.show_error("Invalid credentials!")

    def go_to_sign_up(self, instance):
        self.manager.current = 'sign_up'

    def show_error(self, message):
        popup = Popup(title='Error',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

# Screen for user sign-up
class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20)

        self.username_input = TextInput(hint_text='Choose Username', multiline=False)
        self.password_input = TextInput(hint_text='Choose Password', multiline=False, password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        sign_up_button = Button(text="Sign Up")
        sign_up_button.bind(on_press=self.sign_up)
        layout.add_widget(sign_up_button)

        self.add_widget(layout)

    def sign_up(self, instance):
        username = self.username_input.text
        self.manager.current = 'main'
        self.manager.get_screen('main').label.text = f"Welcome to Brain Buddies, {username}!"

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        # Initial Welcome Label
        self.label = Label(
            text="Welcome to Brain Buddies, [User's Name]!",
            font_size='24sp',
            color=(0.2, 0.6, 0.86, 1),
            bold=True,
        )
        self.layout.add_widget(self.label)

        # Math Challenge Button
        self.math_button = Button(
            text="Start Math Challenge",
            size_hint=(1, 0.2),
            background_color=(0.4, 0.7, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        self.math_button.bind(on_press=self.start_math_challenge)
        self.layout.add_widget(self.math_button)

        # Science Challenge Button
        self.science_button = Button(
            text="Start Science Challenge",
            size_hint=(1, 0.2),
            background_color=(0.8, 0.5, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='20sp'
        )
        self.science_button.bind(on_press=self.start_science_challenge)
        self.layout.add_widget(self.science_button)

        # Answer Input (initially hidden)
        self.answer_input = TextInput(
            hint_text="Enter your answer here",
            multiline=False,
            font_size='18sp',
            foreground_color=(0, 0, 0, 1),
            background_color=(0.9, 0.9, 0.9, 1),
            padding=(10, 10)
        )
        self.answer_input.bind(on_text_validate=self.check_answer)

        # Score Label (initially hidden)
        self.score_label = Label(
            text="Score: 0",
            font_size='20sp',
            color=(0.1, 0.5, 0.1, 1),
            bold=True
        )

        # Initialize state
        self.score = 0
        self.current_question_index = 0
        self.questions = []

        # Add the BoxLayout to the Screen
        self.add_widget(self.layout)
    
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
            user_answer = self.answer_input.text
            current_question = self.questions[self.current_question_index]

            correct_answer = str(current_question["answer"]).strip().lower()
            user_answer = user_answer.strip().lower()

            if user_answer == correct_answer:
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

class BrainBuddiesApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignInScreen(name='sign_in'))
        sm.add_widget(SignUpScreen(name='sign_up'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == "__main__":
    BrainBuddiesApp().run()