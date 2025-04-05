import numpy as np
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173, https://duo-or-not.vercel.app/"])

model = load_model("duolingo_detector.keras")
print("✅ Model loaded")

IMG_SIZE = (224, 224)

def preprocess(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img_bytes = file.read()
    input_tensor = preprocess(img_bytes)

    pred = model.predict(input_tensor)[0][0]
    is_duolingo = pred > 0.5

    return jsonify({
        "prediction": "duolingo" if is_duolingo else "not_duolingo",
        "confidence": float(pred)
    })

if __name__ == "__main__":
    app.run(debug=True)
