import time
import threading

class SyncController:
    def __init__(self, callback, delay=0.02):
        self.callback = callback
        self.delay = delay  # en segundos
        self.last_call_time = 0
        self.lock = threading.Lock()

    def trigger(self):
        with self.lock:
            now = time.time()
            if now - self.last_call_time >= self.delay:
                self.last_call_time = now
                self.callback()
