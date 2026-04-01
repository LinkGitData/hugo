from PIL import Image
import os

source_path = "/Users/yuting/.gemini/antigravity/brain/ef23cb45-4062-4562-96b3-b32135598791/ai_os_cover_1775011771992.png"
target_path = "link-blog/static/images/ai-os-cover.png"

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

try:
    img = Image.open(source_path)
    
    target_width = 1024
    target_height = 256
    
    w_percent = (target_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((target_width, h_size), Image.Resampling.LANCZOS)
    
    if img.size[1] < target_height:
        h_percent = (target_height / float(img.size[1]))
        w_size = int((float(img.size[0]) * float(h_percent)))
        img = img.resize((w_size, target_height), Image.Resampling.LANCZOS)
        img = crop_center(img, target_width, target_height)
    else:
        img = crop_center(img, target_width, target_height)
        
    img.save(target_path)
    print(f"Saved to {target_path}")

except Exception as e:
    print(f"Error: {e}")
