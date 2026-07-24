from PIL import Image

def crop_center(img, target_width, target_height):
    width, height = img.size
    
    # Calculate aspect ratios
    aspect_target = target_width / target_height
    aspect_img = width / height
    
    if aspect_img > aspect_target:
        # Image is wider than target, crop sides
        new_width = int(height * aspect_target)
        left = (width - new_width) / 2
        top = 0
        right = (width + new_width) / 2
        bottom = height
    else:
        # Image is taller than target, crop top/bottom
        new_height = int(width / aspect_target)
        left = 0
        top = (height - new_height) / 2
        right = width
        bottom = (height + new_height) / 2
        
    img_cropped = img.crop((left, top, right, bottom))
    return img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)

input_path = '/Users/yuting/.gemini/antigravity/brain/a4e0c1cc-84eb-4e82-85ec-bb9e5e0dceb6/cloudflare_mcp_cover_1784864558355.jpg'
output_path = '/Users/yuting/Documents/GitHub/hugo/link-blog/static/images/cloudflare-mcp-cover.png'

with Image.open(input_path) as img:
    cropped_img = crop_center(img, 1024, 256)
    cropped_img.save(output_path, 'PNG')
    print(f"Successfully saved cropped image to {output_path}")
