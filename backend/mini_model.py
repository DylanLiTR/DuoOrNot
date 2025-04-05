import tensorflow as tf

model = tf.keras.models.load_model("duolingo_detector.keras")

# Convert to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Optimize for size
tflite_model = converter.convert()

# Save the model
with open("duolingo_detector.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TFLite model saved")
