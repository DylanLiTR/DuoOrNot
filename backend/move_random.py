import os
import random
import shutil

def move_random_images_flat(source, dest, percent=10):
    images = [f for f in os.listdir(source) 
              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    num_to_move = len(images) * percent // 100
    selected = random.sample(images, num_to_move)
    
    os.makedirs(dest, exist_ok=True)
    
    for img in selected:
        shutil.move(os.path.join(source, img), 
                   os.path.join(dest, img))
    
    print("Moved", num_to_move, "images to", dest)

move_random_images_flat("./raw_data/train/not_duolingo", "./raw_data/train/not_duolingo_extra", 50)