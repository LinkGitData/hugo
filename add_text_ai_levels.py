from PIL import Image, ImageDraw, ImageFont
import os

font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
image_path = "/Users/yuting/Documents/GitHub/hugo/link-blog/static/images/ai-users-levels.png"

try:
    img = Image.open(image_path)
    # Ensure image is in RGBA so we can do transparent overlay
    img = img.convert("RGBA")
    
    # Create an overlay layer for transparent backgrounds
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(overlay)
    
    # Try to load font
    try:
        font_size = 48
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Could not load font. Make sure {font_path} exists.")
        exit(1)
        
    draw = ImageDraw.Draw(img)
    
    # Levels and their approximate Y coordinates (from top to bottom)
    levels = [
        {"text": "System Builder", "y": 280},
        {"text": "分析研究型", "y": 480},
        {"text": "效率工具型", "y": 680},
        {"text": "快速答案型", "y": 880}
    ]
    
    image_width = img.width
    
    for level in levels:
        text = level["text"]
        
        # Calculate text bounding box
        # getbbox returns (left, top, right, bottom)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center horizontally
        x = (image_width - text_width) / 2
        y = level["y"]
        
        # Draw background rectangle
        padding_x = 30
        padding_y = 15
        rect_left = x - padding_x
        rect_top = y - padding_y - 10  # offset a bit for box alignment
        rect_right = x + text_width + padding_x
        rect_bottom = y + text_height + padding_y + 10
        
        # Draw semi-transparent rounded-like rect on overlay
        d.rectangle(
            [rect_left, rect_top, rect_right, rect_bottom], 
            fill=(20, 10, 50, 200),  # Dark purple tint with opacity
            outline=(100, 200, 255, 255),  # Cyan glow edge
            width=2
        )
    
    # Merge overlay with original image
    out = Image.alpha_composite(img, overlay)
    
    # Draw text on the composited image
    final_draw = ImageDraw.Draw(out)
    for level in levels:
        text = level["text"]
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        x = (image_width - text_width) / 2
        y = level["y"]
        
        final_draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
    # Drop alpha and save
    out = out.convert("RGB")
    out.save(image_path)
    print("Successfully added text to the image!")

except Exception as e:
    print(f"Error: {e}")
