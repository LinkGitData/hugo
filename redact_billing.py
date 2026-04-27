from PIL import Image, ImageDraw

def redact_natural(image_path, output_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Dashboard is white-ish (#f8f9fa or white)
    # Table names area (x=0-320, y=550-1000)
    # We use a solid white rectangle to make it look like a "clean" column
    draw.rectangle([0, 570, 320, 1024], fill="white")
    
    # Treemap names area (top left chart area)
    # The first bar in the chart and left side of treemap
    draw.rectangle([0, 100, 150, 480], fill="white")
    
    # Specific redaction for any remaining "cola" mentions in the screenshot height
    # Based on the user's latest screenshot, the names are very clear in the table.
    
    img.save(output_path)
    print(f"Natural redaction complete: {output_path}")

redact_natural('link-blog/static/images/gcp-billing-dashboard-anonymized.png', 'link-blog/static/images/gcp-billing-dashboard-anonymized.png')
