import sys
import subprocess
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf"])
    import fitz

pdf_path = "/Users/yuting/Documents/GitHub/hugo/Cloud_Run_Threat_Detection_Essential_Guide.pdf"
out_path = "/Users/yuting/Documents/GitHub/hugo/pdf_text.txt"

doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text() + "\n"

with open(out_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Extracted {len(text)} characters using PyMuPDF. Saved to {out_path}")
