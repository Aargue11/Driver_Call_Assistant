import os
from flask import Flask, send_file, make_response

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Audio server is running on Render!"

@app.route("/audio/<filename>")
def serve_audio(filename):
    file_path = os.path.join("static/audio", filename)
    response = make_response(send_file(file_path))
    response.headers["Content-Type"] = "audio/mpeg"
    response.headers["Content-Disposition"] = f'inline; filename="{filename}"'
    response.headers["Accept-Ranges"] = "bytes"
    return response

# PUERTO Y HOST PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
