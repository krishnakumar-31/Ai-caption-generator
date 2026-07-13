from flask import Flask, request, jsonify
from flask_cors import CORS
from model import generate_caption
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({
        "message": "AI Caption Generator API is running",
        "status": "success",
        "endpoint": "/generate"
    })

@app.route("/generate", methods=["POST"])
def generate():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No image selected"}), 400

    allowed_extensions = {"png", "jpg", "jpeg"}

    extension = file.filename.rsplit(".", 1)[1].lower()

    if extension not in allowed_extensions:
        return jsonify({"error": "Only JPG, JPEG and PNG are allowed"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(filepath)

    try:

        caption = generate_caption(filepath)

        os.remove(filepath)

        return jsonify({
    "status": "success",
    "caption": caption,
    "filename": file.filename,
    "model": "BLIP",
    "message": "Caption generated successfully"
    })

    except Exception as e:

        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "error": str(e)
        }), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
<<<<<<< HEAD
    app.run(host="0.0.0.0", port=port)
=======
    app.run(host="0.0.0.0", port=port)
>>>>>>> 94e63ad (Production configuration)
