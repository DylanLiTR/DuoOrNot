import requests
import os
import time

# 🔹 Unsplash API Key (Get it from https://unsplash.com/developers)
ACCESS_KEY = "MwuS_LDLl04kK33ROtUu5rnmBda8gdRlJzQVJ02XiOA"

# 🔹 Folder to store images
OUTPUT_DIR = "dataset/train/not_duolingo"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🔹 Number of images to download
NUM_IMAGES = 1000

# 🔹 Unsplash API endpoint for random images
URL = f"https://api.unsplash.com/photos/random?count=1&client_id={ACCESS_KEY}"

def download_images(num_images):
    for i in range(num_images):
        try:
            response = requests.get(URL).json()
            if isinstance(response, list):  # Sometimes Unsplash returns a list
                response = response[0]

            img_url = response["urls"]["regular"]
            img_data = requests.get(img_url).content

            with open(f"{OUTPUT_DIR}/image_{i}.jpg", "wb") as f:
                f.write(img_data)

            print(f"✅ Downloaded {i+1}/{num_images}")

            time.sleep(1)  # Prevent API rate limits

        except Exception as e:
            print(f"⚠️ Skipping {i+1}: {e}")
            time.sleep(2)  # Wait before retrying

# 🔹 Start Downloading!
download_images(NUM_IMAGES)
