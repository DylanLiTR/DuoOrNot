# Duo or Not
I created this project to celebrate my 1000-day streak on Duolingo!
https://duo-or-not.vercel.app/

The project includes a data pipeline to scrape, clean, and preprocess images from the internet for training and evaluating the binary classifier. The binary classifier uses MobileNetV2 with frozen weights, but added layers that are trained for binary classification purposes. 

The model achieves a 98% accuracy with a 99% f1-score on images without the Duolingo owl and 94% f1-score on images with the Duolingo owl. 

Here are a few false positives:
![image of false positives](/images/false_positives.png)

Here are a few false negatives:
![image of false negatives](/images/false_negatives.png)

### Weaknesses
It is difficult to collect a variety of types of images (e.g. photos, screenshots, art) and subjects (e.g. animals, toys, games, other objects, websites), so the model may perform poorly on types or subjects it hasn't been trained on. 
