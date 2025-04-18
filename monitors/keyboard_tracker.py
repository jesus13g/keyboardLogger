from pynput import keyboard
import time, threading, re

class KeyboardTracker:
    def __init__(self):
        self.word_count = 0
        self.word_buffer = ""
        self.word_timestamps = []
        self.pause_count = 0
        self.pause_threshold = 3
        self.last_time = time.time()
        self.last_key = None
        self.callback = None

        listener = keyboard.Listener(on_press=self.on_key_press)
        threading.Thread(target=listener.start, daemon=True).start()

    def on_key_press(self, key):
        now = time.time()
        diff = now - self.last_time
        if diff > self.pause_threshold:
            self.pause_count += 1
        self.last_time = now

        print(f"Tecla presionada: {key} . buffer: {self.word_buffer} ")
        try:
            char = key.char
            if char in " \n\t":
                self.last_key = "space" if char == " " else "enter" if char == "\n" else "tab"
                self.count_word()
            elif char.isprintable():
                self.last_key = char.lower()
                self.word_buffer += char
        except AttributeError:
            if key == keyboard.Key.space:
                self.last_key = "space"
                self.count_word()
            elif key == keyboard.Key.enter:
                self.last_key = "enter"
                self.count_word()
            elif key == keyboard.Key.tab:
                self.last_key = "tab"
                self.count_word()
            elif key == keyboard.Key.backspace:
                self.last_key = "backspace"
                self.word_buffer = self.word_buffer[:-1]
            else:
                self.last_key = str(key).replace("Key.", "")


    def count_word(self):
        word = self.word_buffer.strip()
        if re.match(r'^\w+$', word):
            self.word_count += 1
            self.word_timestamps.append(time.time())
            if self.callback:
                self.callback(word)  # ← PASA la palabra
        self.word_buffer = ""




    def get_metrics(self, now):
        def calc_wpm(seconds):
            recent = [t for t in self.word_timestamps if now - t <= seconds]
            return round(len(recent) / (seconds / 60), 2)
        return {
            "words": self.word_count,
            "wpm_10s": calc_wpm(10),
            "wpm_30s": calc_wpm(30),
            "wpm_60s": calc_wpm(60),
            "pauses": self.pause_count,
            "key": self.last_key
        }

    def register_callback(self, cb):
        self.callback = cb
