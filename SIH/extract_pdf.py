import fitz  # pymupdf
import json

doc = fitz.open(r"d:\Testing\Research\SIH_Smart_Automation_Problem_Statements.pdf")

full_text = ""
for page_num, page in enumerate(doc):
    full_text += f"\n=== PAGE {page_num + 1} ===\n"
    full_text += page.get_text()

with open(r"d:\Testing\Research\extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Total pages: {len(doc)}")
print(f"Total chars: {len(full_text)}")
print("Text extracted successfully!")
print("\n--- FULL TEXT ---\n")
print(full_text)
