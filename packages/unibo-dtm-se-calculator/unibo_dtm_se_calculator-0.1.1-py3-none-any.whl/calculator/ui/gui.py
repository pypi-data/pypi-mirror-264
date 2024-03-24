from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from calculator import Calculator


BUTTONS_NAMES = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['.', '0', '=', '+'],
    ['(', 'sqrt', '**', ')'],
]


class CalculatorApp(App):
    def _browse_children(self, container):
        yield container
        if hasattr(container, 'children'):
            for child in container.children:
                yield from self._browse_children(child)
    
    def find_button_by(self, text) -> Button:
        for widget in self._browse_children(self.root):
            if isinstance(widget, Button) and widget.text == text:
                return widget
            
    def build(self):
        self._calc = Calculator()

        grid = BoxLayout(orientation='vertical')
        first_row = BoxLayout()
        grid.add_widget(first_row)

        self.display = Label(text="0", font_size=24, size_hint=(3, 1))
        first_row.add_widget(self.display)

        clear_button = Button(text="C", font_size=24, size_hint=(1, 1), on_press=self.on_button_press)
        first_row.add_widget(clear_button)

        for button_names_row in BUTTONS_NAMES:
            grid_row = BoxLayout()
            for button_name in button_names_row:
                button = Button(text=button_name, font_size=24, on_press=self.on_button_press)
                grid_row.add_widget(button)
            grid.add_widget(grid_row)

        return grid

    def on_button_press(self, button):
        match button.text:
            case "=":
                try:
                    self._calc.compute_result()
                except ValueError as e:
                    self.display.text = "Error"
                    return # do not update the display any further
            case "+":
                self._calc.plus()
            case "-":
                self._calc.minus()
            case "*":
                self._calc.multiply()
            case "/":
                self._calc.divide()
            case ".":
                self._calc.dot()
            case "C":
                self._calc.clear()
            case "(":
                self._calc.open_parenthesis()
            case ")":
                self._calc.close_parenthesis()
            case "sqrt":
                self._calc.square_root()
                self._calc.open_parenthesis()
            case "**":
                self._calc.power()
            case _:
                self._calc.digit(button.text)
        self.display.text = self._calc.expression or "0"


def start_app():
    CalculatorApp().run()


if __name__ == '__main__':
    start_app()
