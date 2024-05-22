from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import logging

app = Flask(__name__)
CORS(
    app, resources={r"/*": {"origins": "http://kicks.local:3000"}}
)  # Specify allowed origin

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Path to the mounted network drive
SAVE_PATH = "/mnt/shared/screenshot.png"


@app.route("/uploads", methods=["POST"])
def upload_image():
    try:
        data = request.get_json()
        if "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        image_data = data["image"]
        # Remove the header (data:image/png;base64,)
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        print(image_data)
        with open(SAVE_PATH, "wb") as image_file:
            image_file.write(image_bytes)

        return jsonify({"message": "Image saved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
