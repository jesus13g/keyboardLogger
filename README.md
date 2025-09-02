# KeyFlow Monitor 🖥️⌨️

**KeyFlow Monitor** es una aplicación tipo *keylogger educativo* que permite registrar y visualizar en tiempo real la actividad del teclado y del ratón.  
Su objetivo principal es **analizar patrones de escritura**, medir la velocidad de tecleo (*WPM*), las pausas, y los clics realizados, mostrando toda la información en una **interfaz web responsiva e interactiva**.

---

![Demo KeyFlow Monitor](docs/imgInterfaz.png)
---

## Funcionamiento

- Captura teclas y clics en segundo plano.

- Calcula métricas: letras escritas, WPM, pausas, clics.

- Envía los datos al navegador con Socket.IO.

- La interfaz (Bootstrap + CSS) muestra un teclado virtual y estadísticas en tiempo real.

## 🛠️ Tecnologías

Python 3, Flask, Flask-SocketIO

pynput (registro de teclado y ratón)

HTML5, Bootstrap 5, CSS3

JavaScript (ES6)

## 📌 Nota

Proyecto con fines educativos y de análisis de escritura.
⚠️ No debe usarse para registrar información sin consentimiento.

## 🚀 Cómo usarlo

1. **Clona este repositorio**
   ```bash
   git clone https://github.com/tuusuario/keyflow-monitor.git


