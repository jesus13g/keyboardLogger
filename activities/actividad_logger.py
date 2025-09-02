import os
from datetime import datetime
import threading

class ActividadLogger:
    def __init__(self, archivo=None):
        if archivo is None:
            # Ruta absoluta segura al archivo logs/actividad.txt
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            logs_dir = os.path.join(project_root, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            archivo = os.path.join(logs_dir, "actividad.txt")

        self.archivo = archivo
        self.click_count = 0
        self.key_count = 0
        self.lock = threading.Lock()
        self.f = None

        try:
            print(f"[INFO] Intentando abrir archivo: {self.archivo}")
            self.f = open(self.archivo, "a", encoding="utf-8", buffering=1)
            print("[INFO] Archivo de actividad abierto correctamente.")
            self.f.write(f"\n\n--- Nuevo registro iniciado: {datetime.now()} ---\n")
        except Exception as e:
            print(f"[ERROR] Fallo al abrir archivo: {e}")
            self.f = None

    def _ahora(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    def registrar_tecla(self, tecla, duracion_ms=None):
        """
        Registra una tecla en una línea con contador y timestamp.
        """
        if not self.f:
            print("[ERROR] Archivo de actividad no disponible para registrar tecla.")
            return

        mapa_especiales = {
            "space": "ESPACIO",
            "enter": "ENTER",
            "tab": "TAB",
            "backspace": "BACKSPACE",
        }
        etiqueta = mapa_especiales.get(tecla.lower(), tecla)

        self.key_count += 1
        ts = self._ahora()

        try:
            with self.lock:
                if duracion_ms is None:
                    self.f.write(f"[KEY {self.key_count}: {etiqueta} @ {ts}]\n")
                else:
                    self.f.write(f"[KEY {self.key_count}: {etiqueta} @ {ts}, {duracion_ms} ms]\n")
                self.f.flush()
        except Exception as e:
            print(f"[ERROR al registrar tecla]: {e}")

    # Alias de compatibilidad (por si en algún sitio aún llamas registrar_palabra)
    def registrar_palabra(self, palabra):
        self.registrar_tecla(palabra)

    def registrar_click(self, tipo, x, y):
        if not self.f:
            print("[ERROR] Archivo de actividad no disponible para registrar click.")
            return

        self.click_count += 1
        ts = self._ahora()

        try:
            with self.lock:
                self.f.write(f"[CLICK {self.click_count}: {tipo} en ({x}, {y}) @ {ts}]\n")
                self.f.flush()
        except Exception as e:
            print(f"[ERROR al registrar click]: {e}")

    def cerrar(self):
        if self.f:
            try:
                self.f.write("--- Fin del registro ---\n")
                self.f.close()
                print("[INFO] Archivo de actividad cerrado correctamente.")
            except Exception as e:
                print(f"[ERROR al cerrar archivo]: {e}")
