import os
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Audio server is running on Render!"

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("static/audio", filename)

# PUERTO Y HOST PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
