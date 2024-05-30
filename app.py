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


def get_incremented_filename(directory, filename):
    base, ext = os.path.splitext(filename)
    counter = 2
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename


@app.route("/uploads", methods=["POST"])
def upload_image():
    try:
        data = request.get_json()
        if "image" not in data:
            return jsonify({"error": "No image provided"}), 400

        if "subfolder" not in data:
            return jsonify({"error": "No subfolder provided"}), 400

        if "printer_id" not in data:
            return jsonify({"error": "No printer_id provided"}), 400

        image_data = data["image"]
        subfolder = data["subfolder"]
        printer_id = data["printer_id"]

        save_dir = f"/mnt/shared/{subfolder}"

        filename = f"{printer_id}.png"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Increment filename if it already exists
        incremented_filename = get_incremented_filename(save_dir, filename)
        save_path = os.path.join(save_dir, incremented_filename)

        # Remove the header (data:image/png;base64,)
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        with open(save_path, "wb") as image_file:
            image_file.write(image_bytes)

        print(f"Image saved to {save_path}")
        base_filename = os.path.splitext(incremented_filename)[0]
        return (
            jsonify(
                {
                    "message": "Image saved successfully",
                    "filename": base_filename,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/next-filename", methods=["GET"])
def get_next_filename():
    try:
        subfolder = request.args.get("subfolder")
        printer_id = request.args.get("printer_id")

        if not subfolder:
            return jsonify({"error": "No subfolder provided"}), 400

        if not printer_id:
            return jsonify({"error": "No printer_id provided"}), 400

        save_dir = f"/mnt/shared/{subfolder}"
        filename = f"{printer_id}.png"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        incremented_filename = get_incremented_filename(save_dir, filename)
        base_filename = os.path.splitext(incremented_filename)[0]

        return jsonify({"next_filename": base_filename}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
