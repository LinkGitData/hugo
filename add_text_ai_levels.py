from PIL import Image, ImageDraw, ImageFont, ImageFilter

font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
image_path = "/Users/yuting/Documents/GitHub/hugo/link-blog/static/images/ai-users-levels.png"
source_raw_path = "/Users/yuting/.gemini/antigravity/brain/ef23cb45-4062-4562-96b3-b32135598791/ai_users_levels_1775018059263.png"

try:
    img = Image.open(source_raw_path).convert("RGBA")
    
    levels = [
        {"text": "System Builder", "subtext": "(1-2%)",  "y": 320,  "size": 26, "sub_size": 20},
        {"text": "分析研究型",      "subtext": "(5-10%)", "y": 480,  "size": 34, "sub_size": 26},
        {"text": "效率工具型",      "subtext": "(20-30%)", "y": 660,  "size": 42, "sub_size": 32},
        {"text": "快速答案型",      "subtext": "(60-70%)", "y": 850,  "size": 52, "sub_size": 38}
    ]
    
    image_width = img.size[0]
    
    shadow_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d_shadow = ImageDraw.Draw(shadow_img)
    
    def draw_text_lines(draw_obj, level, is_shadow=False):
        font_main = ImageFont.truetype(font_path, level["size"])
        font_sub = ImageFont.truetype(font_path, level["sub_size"])
        
        # Draw Main Text
        text = level["text"]
        bbox = font_main.getbbox(text)
        text_w = bbox[2] - bbox[0]
        x = (image_width - text_w) / 2
        y = level["y"]
        
        fill_color = (0, 0, 0, 255) if is_shadow else (255, 255, 255, 245)
        
        draw_obj.text((x, y), text, font=font_main, fill=fill_color)
        if is_shadow:
            draw_obj.text((x-2, y-2), text, font=font_main, fill=fill_color)
            draw_obj.text((x+2, y+2), text, font=font_main, fill=fill_color)
            
        # Draw Subtext just below
        subtext = level["subtext"]
        bbox_sub = font_sub.getbbox(subtext)
        sub_w = bbox_sub[2] - bbox_sub[0]
        sub_x = (image_width - sub_w) / 2
        sub_y = y + bbox[3] - bbox[1] + 5 # 5px padding below main text
        
        draw_obj.text((sub_x, sub_y), subtext, font=font_sub, fill=fill_color)
        if is_shadow:
            draw_obj.text((sub_x-2, sub_y-2), subtext, font=font_sub, fill=fill_color)
            draw_obj.text((sub_x+2, sub_y+2), subtext, font=font_sub, fill=fill_color)
    
    for level in levels:
        draw_text_lines(d_shadow, level, is_shadow=True)

    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(8))
    for _ in range(4):
        img = Image.alpha_composite(img, shadow_img)
    
    text_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d_text = ImageDraw.Draw(text_img)
    
    for level in levels:
        draw_text_lines(d_text, level, is_shadow=False)
        
    img = Image.alpha_composite(img, text_img)
    img = img.convert("RGB")
    img.save(image_path)
    print("Successfully added split text to the image!")

except Exception as e: # pylint: disable=broad-except
    print(f"Error: {e}")
