from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

# Step 1: Convert the document
DOC_SOURCE = "path/to/your/document.md"
converter = DocumentConverter()
doc = converter.convert(source=DOC_SOURCE).document

# Step 2: Initialize the chunker
chunker = HybridChunker()

# Step 3: Chunk the document
chunk_iter = chunker.chunk(dl_doc=doc)

# Step 4: Display chunks
for i, chunk in enumerate(chunk_iter):
    print(f"=== Chunk {i} ===")
    print(f"Chunk Text:\n{chunk.text[:300]}...\n")  # Displaying the first 300 characters
