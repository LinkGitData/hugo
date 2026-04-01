from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
image_path = "/Users/yuting/Documents/GitHub/hugo/link-blog/static/images/ai-users-levels.png"
source_raw_path = "/Users/yuting/.gemini/antigravity/brain/ef23cb45-4062-4562-96b3-b32135598791/ai_users_levels_1775018059263.png"

try:
    img = Image.open(source_raw_path).convert("RGBA")
    
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
    
    levels = [
        {"text": "System Builder", "y": 320,  "size": 36},
        {"text": "分析研究型",      "y": 500,  "size": 44},
        {"text": "效率工具型",      "y": 690,  "size": 52},
        {"text": "快速答案型",      "y": 880,  "size": 60}
    ]
    
    image_width = img.size[0]
    
    # Create an image just for the shadow/glow
    shadow_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d_shadow = ImageDraw.Draw(shadow_img)
    
    # Draw thick shadow text to make it legible against bright background
    for level in levels:
        text = level["text"]
        font = ImageFont.truetype(font_path, level["size"])
        bbox = font.getbbox(text)
        text_w = bbox[2] - bbox[0]
        x = (image_width - text_w) / 2
        y = level["y"]
        d_shadow.text((x, y), text, font=font, fill=(0, 0, 0, 255))
        d_shadow.text((x-2, y-2), text, font=font, fill=(0, 0, 0, 255))
        d_shadow.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 255))

    # Apply Gaussian Blur to create a dark halo (shadow) instead of a hard box
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(8))
    
    # Layer the shadow multiple times to make it darker and more effective
    for _ in range(4):
        img = Image.alpha_composite(img, shadow_img)
    
    # Now draw the bright white text on top
    text_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d_text = ImageDraw.Draw(text_img)
    
    for level in levels:
        text = level["text"]
        font = ImageFont.truetype(font_path, level["size"])
        bbox = font.getbbox(text)
        text_w = bbox[2] - bbox[0]
        x = (image_width - text_w) / 2
        y = level["y"]
        # Add a subtle cyan/purple hue to the text for integration
        # Or just pure white with high opacity
        d_text.text((x, y), text, font=font, fill=(255, 255, 255, 245))
        
    img = Image.alpha_composite(img, text_img)
    
    img = img.convert("RGB")
    img.save(image_path)
    print("Successfully added smooth text to the image!")

except Exception as e:
    print(f"Error: {e}")
