import time
import uuid
from monitors.keyboard_tracker import KeyboardTracker
from monitors.mouse_tracker import MouseTracker
from monitors.sync_controller import SyncController
from activities.actividad_logger import ActividadLogger

class KeyFlowMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.keyboard = KeyboardTracker()
        self.mouse = MouseTracker()
        self.callback = None
        self.sync = None
        self.last_event_type = None
        self.last_key_event = None
        self.last_event_id = None
        self.logger = ActividadLogger()

    def _on_update(self):
        if self.callback:
            self.callback()

    def register_callback(self, callback):
        self.callback = callback
        self.sync = SyncController(callback)

        # Ahora recibimos una tecla por callback (antes era palabra o None)
        self.keyboard.register_callback(lambda key: self._trigger_keyboard(key))
        self.mouse.register_callback(lambda x=None, y=None, tipo=None: self._trigger_mouse(x, y, tipo))

    def _trigger_keyboard(self, key):
        if key:
            print(f"[DEBUG] Tecla detectada: {key}")
            self.last_key_event = key
            # Si actualizaste ActividadLogger con registrar_tecla, usa esto:
            self.logger.registrar_tecla(key)
            # Si aún no lo actualizaste, podrías usar:
            # self.logger.registrar_palabra(key)
        self.last_event_id = uuid.uuid4().hex
        if self.sync:
            self.sync.trigger()

    def _trigger_mouse(self, x, y, tipo):
        print(f"[DEBUG] Click detectado: {tipo} en ({x},{y})")
        self.last_key_event = tipo
        self.logger.registrar_click(tipo, x, y)
        self.last_event_id = uuid.uuid4().hex
        if self.sync:
            self.sync.trigger()

    def get_metrics(self):
        now = time.time()
        keyboard_metrics = self.keyboard.get_metrics(now)
        mouse_metrics = self.mouse.get_metrics()

        elapsed = now - self.start_time
        # “wpm” ahora es realmente KPM (teclas por minuto) para compatibilidad
        wpm_total = keyboard_metrics["words"] / (elapsed / 60) if elapsed > 0 else 0

        result = {
            **keyboard_metrics,
            **mouse_metrics,
            "wpm": round(wpm_total, 2),  # en realidad KPM
            "key": self.last_key_event,
            "pressed": keyboard_metrics.get("pressed"),
            "event_id": self.last_event_id
        }

        self.last_key_event = None
        self.keyboard.last_pressed_key = None

        return result
