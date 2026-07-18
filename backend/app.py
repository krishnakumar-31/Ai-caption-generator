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

    # Check if image is present
    if "image" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No image uploaded"
        }), 400

    file = request.files["image"]

    # Check filename
    if file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No image selected"
        }), 400

    # Validate extension
    allowed_extensions = {"png", "jpg", "jpeg"}

    if "." not in file.filename:
        return jsonify({
            "status": "error",
            "message": "Invalid file"
        }), 400

    extension = file.filename.rsplit(".", 1)[1].lower()

    if extension not in allowed_extensions:
        return jsonify({
            "status": "error",
            "message": "Only PNG, JPG and JPEG files are allowed"
        }), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        # Save uploaded image
        file.save(filepath)

        # Generate caption
        caption = generate_caption(filepath)

        # Delete uploaded image
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "status": "success",
            "caption": caption,
            "filename": file.filename,
            "model": "BLIP",
            "message": "Caption generated successfully"
        })

    except Exception as e:

        # Delete uploaded image if an error occurs
        if os.path.exists(filepath):
            os.remove(filepath)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)