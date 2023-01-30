import io
import base64
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from flask_cors import CORS

UPLOAD_FOLDER = "./temp"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "JPG", "JPEG", "PNG"])

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def reset_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        for f in os.listdir(dir):
            if allowed_file(f):
                os.remove(os.path.join(dir, f))


@app.route("/api/ping")
def ping():
    return "pong"


@app.route("/api/predict", methods=["POST"])
def detect():
    name = None
    file = request.files.get("file")
    print(file)
    if file and allowed_file(file.filename):
        name = secure_filename(file.filename)
        print(os.path.join(UPLOAD_FOLDER, name))
        file.save(os.path.join(UPLOAD_FOLDER, name))

    json = {}

    if name is None:
        json["error"] = "No file uploaded"
        return jsonify(json)

    im_io = io.BytesIO()

    ## return image in base64
    pred_img = Image.open(os.path.join(UPLOAD_FOLDER, name))
    pred_img = pred_img.convert("RGBA")
    pred_img.save(im_io, "PNG")
    im_io.seek(0)
    image_url = base64.b64encode(im_io.getvalue()).decode()
    json["base64"] = "data:image/png;base64, " + image_url

    return jsonify(json)

    ## just return json
    # pred_json = {"boxes": [[0, 0, 100, 100], [100, 100, 200, 200]]}
    # return jsonify(pred_json)


if __name__ == "__main__":
    reset_dir(UPLOAD_FOLDER)
    app.run(debug=True)
