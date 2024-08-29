from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyKivyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Welcome to Brain Buddies!")
        layout.add_widget(self.label)

        # Math Challenge Button
        math_button = Button(text="Start Math Challenge")
        math_button.bind(on_press=self.start_math_challenge)
        layout.add_widget(math_button)

        # Science Challenge Button
        science_button = Button(text="Start Science Challenge")
        science_button.bind(on_press=self.start_science_challenge)
        layout.add_widget(science_button)

        return layout
    
    def start_math_challenge(self, instance):
        self.label.text = "Math Challenge Started!"
    
    def start_science_challenge(self, instance):
        self.label.text = "Science Challenge Started!"

if __name__ == "__main__":
    MyKivyApp().run()