from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyKivyApp(App):
    def build(self):
        self.label = Label(text="Hello, Kivy!")
        button = Button(text="Click me!")

        button.bind(on_press=self.update_label)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(button)

        return layout
    
    def update_label(self, instance):
        self.label.text = "Button clicked!"
    
if __name__ == "__main__":
    MyKivyApp().run()