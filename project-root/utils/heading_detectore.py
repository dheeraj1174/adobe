def detect_headings(blocks):
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
        level = size_to_level.get(block["size"])
        if level == "Title" and not title:
            title = block["text"]
        elif level in ["H1", "H2", "H3"]:
            outline.append({
                "level": level,
                "text": block["text"],
                "page": block["page"]
            })

    return title, outline
