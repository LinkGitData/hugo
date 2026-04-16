import os
from PIL import Image

def process_cover_image(input_path, output_path, target_width=1024, target_height=256):
    if not os.path.exists(input_path):
        print(f"Error: Input image not found at {input_path}")
        print("Please place your generated cover image there and run this script again.")
        return

    with Image.open(input_path) as img:
        # Calculate aspect ratios
        target_ratio = target_width / target_height
        img_ratio = img.width / img.height

        if img_ratio > target_ratio:
            # Image is wider than target, crop width
            new_width = int(target_ratio * img.height)
            left = (img.width - new_width) / 2
            top = 0
            right = (img.width + new_width) / 2
            bottom = img.height
        else:
            # Image is taller than target, crop height
            new_height = int(img.width / target_ratio)
            left = 0
            top = (img.height - new_height) / 2
            right = img.width
            bottom = (img.height + new_height) / 2

        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))
        
        # Resize to target dimensions
        final_img = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_img.save(output_path)
        print(f"✅ Successfully processed image!")
        print(f"Source: {input_path} ({img.width}x{img.height})")
        print(f"Output: {output_path} ({target_width}x{target_height})")

if __name__ == "__main__":
    # Source image to read
    input_file = "/Users/yuting/Documents/GitHub/hugo/cloud-run-crtd-cover-source.png"
    # Target path inside Hugo
    output_file = "/Users/yuting/Documents/GitHub/hugo/link-blog/static/images/cloud-run-crtd-cover.png"
    
    print("Looking for source image...")
    process_cover_image(input_file, output_file)
