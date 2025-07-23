# PDF Outline Extractor

## How it Works

- Parses all PDFs from `/app/input`
- Extracts title, H1–H3 headings with page numbers
- Outputs JSON to `/app/output`

## Run (auto-run via Docker)
```bash
docker build --platform linux/amd64 -t pdf-outliner:latest .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outliner:latest
