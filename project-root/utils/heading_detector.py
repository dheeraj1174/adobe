def is_heading(text, size):
    if text.strip().lower() == "overview":
        return True
    # existing checks...
    if len(text.strip()) < 3:
        return False
    if text.strip().isdigit():
        return False
    # font size based threshold bhi laga sakte ho
    if size < 10:  # example threshold
        return False
    return True


def detect_headings(blocks):
    # blocks is a list of dicts with keys: text, size, page
    sizes = list(set([b["size"] for b in blocks]))
    sizes.sort(reverse=True)

    if not sizes:
        return "", []

    size_to_level = {}
    if len(sizes) > 0: size_to_level[sizes[0]] = "Title"
    if len(sizes) > 1: size_to_level[sizes[1]] = "H1"
    if len(sizes) > 2: size_to_level[sizes[2]] = "H2"
    if len(sizes) > 3: size_to_level[sizes[3]] = "H3"

    title = ""
    outline = []
    for block in blocks:
        text = block["text"]
        if not is_heading(text):
            continue  # Skip non-heading text

        level = size_to_level.get(block["size"])
        if level == "Title" and not title:
            title = text
        elif level in ["H1", "H2", "H3"]:
            outline.append({
                "level": level,
                "text": text,
                "page": block["page"]
            })

    return title, outline
