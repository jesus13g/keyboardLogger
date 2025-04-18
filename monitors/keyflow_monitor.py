import time
import uuid 
from monitors.keyboard_tracker import KeyboardTracker
from monitors.mouse_tracker import MouseTracker
from monitors.sync_controller import SyncController

class KeyFlowMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.keyboard = KeyboardTracker()
        self.mouse = MouseTracker()
        self.callback = None
        self.sync = None
        self.last_event_type = None  # 'keyboard' o 'mouse'
        self.last_key_event = None
        self.last_event_id = None  # identificador único por evento


    def _on_update(self):
        if self.callback:
            self.callback()

    def register_callback(self, callback):
        self.callback = callback
        self.sync = SyncController(callback)
        self.keyboard.register_callback(lambda word: self._trigger_from("keyboard", word))
        self.mouse.register_callback(lambda: self._trigger_from("mouse"))



    def _trigger_from(self, source, word=None):
        if source == "mouse" and self.mouse.last_click:
            self.last_key_event = self.mouse.last_click
        elif source == "keyboard" and word:
            self.last_key_event = word

        self.last_event_id = uuid.uuid4().hex

        if self.sync:
            self.sync.trigger()



    def get_metrics(self):
        now = time.time()
        keyboard_metrics = self.keyboard.get_metrics(now)
        mouse_metrics = self.mouse.get_metrics()

        elapsed = now - self.start_time
        wpm_total = keyboard_metrics["words"] / (elapsed / 60) if elapsed > 0 else 0

        return {
            **keyboard_metrics,
            **mouse_metrics,
            "wpm": round(wpm_total, 2),
            "key": self.last_key_event,
            "event_id": self.last_event_id  # ← importante
        }