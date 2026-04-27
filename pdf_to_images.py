import fitz
import os

pdf_path = "/Users/yuting/Documents/GitHub/hugo/Cloud_Run_Threat_Detection_Essential_Guide.pdf"
out_dir = "/Users/yuting/Documents/GitHub/hugo/pdf_images"

os.makedirs(out_dir, exist_ok=True)
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
for i in range(min(len(doc), 15)): # limit to 15 pages to save time/space
    page = doc[i]
    pix = page.get_pixmap(dpi=150) # render at 150 dpi
    out_file = os.path.join(out_dir, f"page_{i:02d}.png")
    pix.save(out_file)
    print(f"Saved {out_file}")

print("Done generating images.")
