from flask import Flask, render_template
from flask_socketio import SocketIO
from monitors.keyflow_monitor import KeyFlowMonitor
from models import init_db, save_metrics

app = Flask(__name__)
app.config['SECRET_KEY'] = 'keyflow-secret'
socketio = SocketIO(app, async_mode='threading')

init_db()
monitor = KeyFlowMonitor()

@app.route('/')
def index():
    return render_template('index.html')

last_key_saved = None  # ← aquí guardamos el valor anterior

def send_metrics():
    metrics = monitor.get_metrics()
    print(f"Envío de métricas: {metrics}")
    save_metrics(metrics)
    socketio.emit('update', metrics)


if __name__ == '__main__':
    monitor.register_callback(send_metrics)
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)  # ← debug desactivado


