from PIL import Image
import os

img_path = "/Users/yuting/.gemini/antigravity/brain/e9f1f271-5f0b-44b4-975e-29d1ce259fed/gateway_vs_armor_cover_1777864566932.png"
output_dir = "/Users/yuting/Documents/GitHub/hugo/link-blog/static/images"
output_path = os.path.join(output_dir, "ai-gateway-vs-model-armor-cover.png")

os.makedirs(output_dir, exist_ok=True)
img = Image.open(img_path)

target_width = 1024
target_height = 256
target_ratio = target_width / target_height

width, height = img.size
current_ratio = width / height

if current_ratio > target_ratio:
    new_width = int(target_ratio * height)
    offset = (width - new_width) / 2
    crop_box = (offset, 0, width - offset, height)
else:
    new_height = int(width / target_ratio)
    offset = (height - new_height) / 2
    crop_box = (0, offset, width, height - offset)

img_cropped = img.crop(crop_box)
img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
img_resized.save(output_path)
print(f"Image successfully cropped and saved to {output_path}")
