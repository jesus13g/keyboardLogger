from pynput import keyboard
import time, threading, re

class KeyboardTracker:
    def __init__(self):
        # Antes: word_count/word_buffer/word_timestamps
        # Ahora: contamos teclas individuales
        self.key_count = 0
        self.key_timestamps = []

        self.pause_count = 0
        self.pause_threshold = 3  # segs sin pulsar = pausa
        self.last_time = time.time()
        self.last_key = None
        self.last_pressed_key = None
        self.callback = None

        listener = keyboard.Listener(on_press=self.on_key_press)
        threading.Thread(target=listener.start, daemon=True).start()

    def _emit_key(self, label: str):
        """Registra y emite una tecla individual."""
        now = time.time()
        diff = now - self.last_time
        if diff > self.pause_threshold:
            self.pause_count += 1
        self.last_time = now

        self.key_count += 1
        self.key_timestamps.append(now)
        self.last_key = label
        self.last_pressed_key = label

        if self.callback:
            self.callback(label)

    def on_key_press(self, key):
        # print(f"Key pressed: {key}")  # si molesta, coméntalo
        try:
            # Teclas imprimibles
            char = key.char
            if char in " \n\t":
                # Espacio / Enter / Tab como etiquetas canónicas
                label = "space" if char == " " else "enter" if char == "\n" else "tab"
                self._emit_key(label)
            elif char.isprintable():
                # Letra, número, etc. Normalizamos a minúscula
                self._emit_key(char.lower())
        except AttributeError:
            # Teclas especiales (no imprimibles)
            if key == keyboard.Key.space:
                self._emit_key("space")
            elif key == keyboard.Key.enter:
                self._emit_key("enter")
            elif key == keyboard.Key.tab:
                self._emit_key("tab")
            elif key == keyboard.Key.backspace:
                self._emit_key("backspace")
            else:
                # Otros: shift, ctrl, alt, etc.
                label = str(key).replace("Key.", "")
                self._emit_key(label)

    def get_metrics(self, now):
        def calc_kpm(seconds):
            recent = [t for t in self.key_timestamps if now - t <= seconds]
            return round(len(recent) / (seconds / 60), 2)

        return {
            # Para no romper código externo, “words” ahora = número de teclas
            "words": self.key_count,
            "wpm_10s": calc_kpm(10),   # realmente KPM
            "wpm_30s": calc_kpm(30),
            "wpm_60s": calc_kpm(60),
            "pauses": self.pause_count,
            "key": self.last_key,
            "pressed": self.last_pressed_key
        }

    def register_callback(self, cb):
        self.callback = cb
