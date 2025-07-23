import fitz

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []
    for page_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    text = " ".join([span["text"] for span in line["spans"]])
                    if text.strip():
                        size = line["spans"][0]["size"]
                        font = line["spans"][0]["font"]
                        blocks.append({
                            "text": text.strip(),
                            "size": size,
                            "font": font,
                            "page": page_num
                        })
    return blocks
