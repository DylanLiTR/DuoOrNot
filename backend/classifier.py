import ssl
from utils import preprocess_images
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
import matplotlib.pyplot as plt

# Fix SSL certificate issue on Mac
ssl._create_default_https_context = ssl._create_unverified_context

preprocess_images("./raw_data/train/duolingo", "./dataset/train/duolingo")
preprocess_images("./raw_data/train/not_duolingo", "./dataset/train/not_duolingo")
preprocess_images("./raw_data/validation/duolingo", "./dataset/validation/duolingo")
preprocess_images("./raw_data/validation/not_duolingo", "./dataset/validation/not_duolingo")

# Load training & validation datasets
train_ds = image_dataset_from_directory(
    "./dataset/train",
    image_size=(224, 224),
    batch_size=32,
    class_names = ["not_duolingo", "duolingo"]
)

val_ds = image_dataset_from_directory(
    "./dataset/validation",
    image_size=(224, 224),
    batch_size=32,
    shuffle=False,
    class_names = ["not_duolingo", "duolingo"]
)

# Normalize pixel values (0 to 1)
train_ds = train_ds.map(lambda x, y: (tf.keras.applications.mobilenet_v2.preprocess_input(x), y))
val_ds = val_ds.map(lambda x, y: (tf.keras.applications.mobilenet_v2.preprocess_input(x), y))

# Load MobileNetV2 with pre-trained weights
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)
base_model.trainable = False  # Freeze base model layers

# Add classification layers
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation="sigmoid")  # Binary classification (duolingo / not_duolingo)
])

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

class_weight = {
    0: (4000 + 2000) / 2000,  # "Duolingo" (minority)
    1: 1.0  # "Not Duolingo" (majority)
}

# Train the model
history = model.fit(train_ds, validation_data=val_ds, epochs=10, class_weight=class_weight)
model.save("duolingo_detector.keras")

# Plot training history
def plot_training_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

plot_training_history(history)
