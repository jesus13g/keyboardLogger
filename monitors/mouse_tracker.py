from pynput import mouse
from pynput.mouse import Button
import threading

class MouseTracker:
    def __init__(self):
        self.left_clicks = 0
        self.right_clicks = 0
        self.callback = None
        self.last_click = None

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
                self.callback(x, y, self.last_click)

    def get_metrics(self):
        return {
            "clicks_left": self.left_clicks,
            "clicks_right": self.right_clicks,
            "last_click": self.last_click
        }

    def register_callback(self, callback):
        self.callback = callback
