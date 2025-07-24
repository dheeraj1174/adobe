import fitz  # PyMuPDF
import os
import json
import time

# ---- Utility Functions ----
def is_heading(text):
    return len(text.strip()) >= 3 and not text.strip().isdigit()

def get_font_size_dict(page):
    blocks = page.get_text("dict")["blocks"]
    headings = []
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text").strip()
                size = span.get("size")
                if text and is_heading(text):
                    headings.append({"text": text, "size": size})
    return headings

def extract_outline(pdf_path):
    print(f"Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"Total pages in PDF: {len(doc)}")

    headings = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        spans = get_font_size_dict(page)
        for span in spans:
            headings.append({
                "text": span["text"],
                "size": span["size"],
                "page": page_num + 1
            })

    unique_sizes = sorted(set([h["size"] for h in headings]), reverse=True)
    print(f"Unique font sizes found: {unique_sizes}")

    top_sizes = unique_sizes[:3]
    size_to_level = {size: ("H1" if size == top_sizes[0] else "H2" if size == top_sizes[1] else "H3")
                     for size in unique_sizes}

    outline = []
    current_h1, current_h2 = None, None

    for h in headings:
        level = size_to_level.get(h["size"])
        if not level:
            continue
        text, page = h["text"], h["page"]

        if level == "H1":
            current_h1 = {"level": level, "text": text, "page": page, "children": []}
            outline.append(current_h1)
            current_h2 = None
        elif level == "H2":
            h2_item = {"level": level, "text": text, "page": page, "children": []}
            if current_h1:
                current_h1["children"].append(h2_item)
                current_h2 = h2_item
            else:
                outline.append(h2_item)
                current_h2 = h2_item
        else:
            h3_item = {"level": level, "text": text, "page": page}
            if current_h2:
                current_h2["children"].append(h3_item)
            elif current_h1:
                current_h1["children"].append(h3_item)
            else:
                outline.append(h3_item)

    title = outline[0]["text"] if outline else doc.metadata.get("title", "Untitled Document")
    return {"title": title, "outline": outline}

# ---- Main Execution ----
if __name__ == "__main__":
    start_time = time.time()

    input_folder = "input"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Auto-detect first PDF in input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("No PDF found in input folder!")
        exit(1)

    pdf_name = pdf_files[0]
    input_pdf_path = os.path.join(input_folder, pdf_name)
    output_file_path = os.path.join(output_folder, pdf_name.replace(".pdf", "_outline.json"))

    print(f"Processing file: {pdf_name}")
    outline_json = extract_outline(input_pdf_path)

    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(outline_json, f, indent=4, ensure_ascii=False)

    end_time = time.time()
    print(f"✅ Outline saved to {output_file_path}")
    print(f"⏱ Execution Time: {end_time - start_time:.2f} seconds")
