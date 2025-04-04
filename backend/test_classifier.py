import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory
import numpy as np
from sklearn.metrics import classification_report
from utils import preprocess_images
import matplotlib.pyplot as plt

preprocess_images("./raw_data/test/duolingo", "./dataset/test/duolingo")
preprocess_images("./raw_data/test/not_duolingo", "./dataset/test/not_duolingo")

model = load_model("duolingo_detector.keras")
print("✅ Model Loaded!")

test_ds = image_dataset_from_directory(
    "./dataset/test",
    image_size=(224, 224),
    batch_size=32,
    shuffle=False,
    class_names = ["not_duolingo", "duolingo"]
)

# Normalize pixel values
test_ds = test_ds.map(lambda x, y: (tf.keras.applications.mobilenet_v2.preprocess_input(x), y))

test_loss, test_accuracy = model.evaluate(test_ds)
print(f"📊 Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"📉 Test Loss: {test_loss:.4f}")

# Get true labels and predictions
images, y_true = [], []
for x, y in test_ds:
    images.append(x.numpy())
    y_true.append(y.numpy())
images = np.concatenate(images)
y_true = np.concatenate(y_true)
y_pred = model.predict(test_ds)
y_pred = np.round(y_pred).flatten()  # Convert probabilities to 0/1 labels

# Generate a classification report
print(classification_report(y_true, y_pred, target_names=["Not Duolingo", "Duolingo"]))

# Visualize misclassifications
def visualize_misclassifications(images, y_true, y_pred):
    false_positives = []
    false_negatives = []
    
    for i in range(len(y_true)):
        if y_true[i] == 0 and y_pred[i] == 1:  # False Positive
            false_positives.append(i)
        elif y_true[i] == 1 and y_pred[i] == 0:  # False Negative
            false_negatives.append(i)
    
    # Plot False Positives
    if false_positives:
        print(f"False Positives (Predicted Duolingo, Actually Not Duolingo): {len(false_positives)}")
        plt.figure(figsize=(15, 5))
        for j, idx in enumerate(false_positives[:5]):  # Show up to 5 examples
            plt.subplot(1, 5, j+1)
            img = images[idx] * 0.5 + 0.5  # Denormalize from [-1, 1] to [0, 1] for display
            plt.imshow(img)
            plt.title(f"FP #{idx}")
            plt.axis('off')
        plt.show()
    
    # Plot False Negatives
    if false_negatives:
        print(f"False Negatives (Predicted Not Duolingo, Actually Duolingo): {len(false_negatives)}")
        plt.figure(figsize=(15, 5))
        for j, idx in enumerate(false_negatives[:5]):  # Show up to 5 examples
            plt.subplot(1, 5, j+1)
            img = images[idx] * 0.5 + 0.5  # Denormalize
            plt.imshow(img)
            plt.title(f"FN #{idx}")
            plt.axis('off')
        plt.show()

visualize_misclassifications(images, y_true, y_pred)
