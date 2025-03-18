import re

class ParagraphTextSplitter:
    def __init__(self, max_paragraphs=None, max_tokens=None, chunk_overlap=0):
        """
        Initialize the ParagraphTextSplitter.

        Args:
            max_paragraphs (int): Maximum number of paragraphs per chunk.
            max_tokens (int): Maximum number of tokens per chunk (approximate).
            chunk_overlap (int): Number of paragraphs to overlap between chunks.
        """
        self.max_paragraphs = max_paragraphs
        self.max_tokens = max_tokens
        self.chunk_overlap = chunk_overlap

    def _count_tokens(self, text):
        # Approximate token count using whitespace split
        return len(text.split())

    def split(self, text):
        paragraphs = re.split(r'\n\s*\n+', text.strip())  # Split on paragraph breaks
        chunks = []
        current_chunk = []

        for i, paragraph in enumerate(paragraphs):
            if self.max_paragraphs and len(current_chunk) >= self.max_paragraphs:
                # Add current chunk to the list and reset
                chunks.append("\n\n".join(current_chunk))
                current_chunk = current_chunk[-self.chunk_overlap:]  # Keep the overlap

            current_chunk.append(paragraph)
            current_text = "\n\n".join(current_chunk)

            if self.max_tokens and self._count_tokens(current_text) > self.max_tokens:
                # If token limit exceeded, remove last paragraph and finalize the chunk
                current_chunk.pop()
                chunks.append("\n\n".join(current_chunk))
                current_chunk = current_chunk[-self.chunk_overlap:] + [paragraph]

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))  # Add the last chunk

        return chunks

# Example usage
if __name__ == "__main__":
    text = """
    This is the first paragraph.

    This is the second paragraph. It has some more content to make it longer.

    Here's the third paragraph, which is a bit shorter.

    And finally, the fourth paragraph for testing.
    """

    splitter = ParagraphTextSplitter(max_paragraphs=2, max_tokens=50, chunk_overlap=1)
    chunks = splitter.split(text)
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n{'-' * 40}")
