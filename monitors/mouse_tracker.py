from pynput import mouse
from pynput.mouse import Button
import threading

class MouseTracker:
    def __init__(self):
        self.left_clicks = 0
        self.right_clicks = 0
        self.callback = None  # nuevo
        self.last_click = None  # para registrar qué tipo de clic fue


        listener = mouse.Listener(on_click=self.on_click)
        threading.Thread(target=listener.start, daemon=True).start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == Button.left:
                self.left_clicks += 1
                self.last_click = "ClickIzq"
            elif button == Button.right:
                self.right_clicks += 1
                self.last_click = "ClickDrch"

            if self.callback:
                self.callback()


    def get_metrics(self):
        click_info = {
            "clicks_left": self.left_clicks,
            "clicks_right": self.right_clicks,
            "last_click": self.last_click
        }
        return click_info


    def register_callback(self, callback):  # nuevo
        self.callback = callback
