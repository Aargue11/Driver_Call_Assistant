from flask import Flask, send_from_directory

app = Flask(__name__)

# Ruta para servir archivos de audio
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

# Ruta de prueba
@app.route('/')
def index():
    return "🚛 Audio server is running!"

# Ejecutar localmente
if __name__ == '__main__':
    app.run(debug=True)
