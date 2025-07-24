import os
from utils.parser import extract_text_blocks
from utils.heading_detector import detect_headings
from utils.json_writer import write_json
import time

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def process_pdf(pdf_path, output_path):
    blocks = extract_text_blocks(pdf_path)
    title, outline = detect_headings(blocks)
    write_json(title, outline, output_path)

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    for file in os.listdir(INPUT_DIR):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, file)
            output_file = file.replace(".pdf", ".json")
            output_path = os.path.join(OUTPUT_DIR, output_file)
            process_pdf(pdf_path, output_path)

if __name__ == "__main__":
    main()

start_time = time.time()

# ---- your main code ----
# For example:
print("Processing PDF...")
# Your extraction function
# -------------------------

end_time = time.time()
print(f"Execution Time: {end_time - start_time:.2f} seconds")