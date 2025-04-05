import numpy as np
import tensorflow as tf
from PIL import Image
import io
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "https://duo-or-not.vercel.app/"])

IMG_SIZE = (224, 224)

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="duolingo_detector.tflite")
interpreter.allocate_tensors()
input_index = interpreter.get_input_details()[0]["index"]
output_index = interpreter.get_output_details()[0]["index"]
print("✅ TFLite model loaded")

def preprocess(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    img = img.resize(IMG_SIZE)
    img_array = np.array(img, dtype=np.float32) / 127.5 - 1  # MobileNetV2 preprocessing
    return np.expand_dims(img_array, axis=0)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img_bytes = request.files["image"].read()
    input_tensor = preprocess(img_bytes)

    # Run inference with TFLite
    interpreter.set_tensor(input_index, input_tensor)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_index)[0][0]

    return jsonify({
        "prediction": "duolingo" if pred > 0.5 else "not_duolingo",
        "confidence": float(pred)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
