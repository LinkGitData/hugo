from PIL import Image
import os

source_path = "/Users/yuting/.gemini/antigravity/brain/69862f0d-78dc-4625-acfa-90449e6ac9d4/gemini_anime_cover_raw_1765330573763.png"
target_path = "link-blog/static/images/gemini-cover.png"

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

try:
    img = Image.open(source_path)
    print(f"Original size: {img.size}")
    
    # Target dimensions
    target_date_width = 1024
    target_height = 256
    
    # Strategy: Resize to width 1024, maintaining aspect ratio.
    # Then crop vertical center.
    w_percent = (target_date_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((target_date_width, h_size), Image.Resampling.LANCZOS)
    print(f"Resized to width 1024: {img.size}")
    
    if img.size[1] < target_height:
        print("Warning: Image height is less than target height after resize. Scaling by height instead.")
        # If height is too small, scale by height first
        h_percent = (target_height / float(img.size[1]))
        w_size = int((float(img.size[0]) * float(h_percent)))
        img = img.resize((w_size, target_height), Image.Resampling.LANCZOS)
        # Then crop width
        img = crop_center(img, target_date_width, target_height)
    else:
        # Crop center height
        img = crop_center(img, target_date_width, target_height)
        
    print(f"Final size: {img.size}")
    img.save(target_path)
    print(f"Saved to {target_path}")

except Exception as e:
    print(f"Error: {e}")
