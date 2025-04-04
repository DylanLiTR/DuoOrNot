from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
import io
from PIL import Image
import hashlib
import re

def fetch_image_urls(query, max_links_to_fetch, driver):
    # Build the Google search URL for images
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    
    # Navigate to the search URL
    driver.get(search_url)
    
    # Scroll down to load more images
    image_count = 0
    results_start = 0
    
    while image_count < max_links_to_fetch:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for page to load
        
        # Get all image thumbnail elements
        thumbnail_results = driver.find_elements(By.CSS_SELECTOR, "img")
        
        # Count the number of results now visible
        number_results = len(thumbnail_results)
        
        print(f"Found {number_results} results. Extracting links from {results_start}:{max_links_to_fetch}")
        
        # Click each thumbnail to get the full-size image
        for img in thumbnail_results[results_start:number_results]:
            # Try to click the image
            try:
                driver.execute_script("arguments[0].click();", img)
                time.sleep(1)  # Wait for full-size image to load
            except Exception as e:
                print(f"Error clicking image: {e}")
                continue
            
            # Try to get the full-size image URL
            try:
                # Wait for large image to appear
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c"))
                )
                
                # Get the full-size image URL
                actual_images = driver.find_elements(By.CSS_SELECTOR, "img.sFlh5c")
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        yield actual_image.get_attribute('src')
                        image_count += 1
            except Exception as e:
                print(f"Error getting image URL: {e}")
            
            if image_count >= max_links_to_fetch:
                break
        
        # Update results_start for the next batch
        results_start = number_results
        
        # If we're not getting new results, break
        if results_start == number_results:
            print("No more results available.")
            break

def download_image(folder_path, url):
    try:
        # Download the image
        image_content = requests.get(url, timeout=30).content
        
        # Convert to an image
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        
        # Create a unique file name using hash of image URL
        file_path = os.path.join(folder_path, hashlib.sha1(url.encode()).hexdigest()[:10] + '.jpg')
        
        # Save the image
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        
        print(f"SUCCESS - saved {url} as {file_path}")
        return True
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        return False

def search_and_download(query, driver, target_path, number_images=100):
    # Create the target directory if it doesn't exist
    # target_folder = os.path.join(target_path, '_'.join(query.lower().split(' ')))
    # if not os.path.exists(target_folder):
    #     os.makedirs(target_folder)
    
    # Get image URLs
    image_urls = fetch_image_urls(query, number_images, driver)
    
    # Download images
    downloaded_count = 0
    for url in image_urls:
        if download_image(target_path, url):
            downloaded_count += 1
        
        if downloaded_count >= number_images:
            break
    
    print(f"Downloaded {downloaded_count} images for {query}")
    return downloaded_count

def main():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode if desired
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set up Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Where to save the images
    output_path = './dataset/owl'
    
    # Search queries to get various angles and styles of the Duolingo owl
    queries = [
        "Duolingo owl mascot",
        "Duolingo owl Duo",
        "Duolingo owl character",
        "Duolingo owl meme",
        "Duolingo green owl"
    ]
    
    # Download images for each query
    for query in queries:
        search_and_download(query, driver, output_path, number_images=50)
    
    # Close the driver
    driver.quit()
    
    print("Image scraping complete!")

if __name__ == "__main__":
    main()