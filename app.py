from flask import Flask, render_template
from flask_socketio import SocketIO
from monitors.keyflow_monitor import KeyFlowMonitor

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

monitor = KeyFlowMonitor()

@app.route('/')
def index():
    return render_template('index.html')

def send_metrics():
    metrics = monitor.get_metrics()
    socketio.emit('update', metrics)

if __name__ == '__main__':
    try:
        monitor.register_callback(send_metrics)
        socketio.run(app, host='127.0.0.1', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n[INFO] Aplicación detenida por el usuario.")
    except Exception as e:
        print(f"\n[ERROR] Excepción durante la ejecución: {e}")
    finally:
        if hasattr(monitor, "logger") and monitor.logger:
            print("[INFO] Cerrando archivo de registro...")
            monitor.logger.cerrar()
