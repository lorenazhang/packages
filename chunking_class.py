import re

class BaseChunker:
    def __init__(self, min_tokens=20, max_tokens=300):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
    
    def _combine_chunks(self, tokens):
        chunks = []
        current_chunk = []
        current_token_count = 0
        
        for token in tokens:
            if current_token_count + len(token.split()) > self.max_tokens:
                # Split if exceeding max tokens
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_token_count = 0
            
            current_chunk.append(token)
            current_token_count += len(token.split())
            
            # Allow split if we reached min_tokens
            if current_token_count >= self.min_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_token_count = 0
        
        # Add any remaining tokens
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks


class ParagraphChunker(BaseChunker):
    def chunk(self, text):
        # Split by paragraph markers (\n\n or multiple newlines)
        paragraphs = re.split(r'\n{2,}', text.strip())
        return self._combine_chunks(paragraphs)


class SectionChunker(BaseChunker):
    def __init__(self, section_pattern=r'(^#\s|^##\s|^===)', min_tokens=20, max_tokens=500):
        super().__init__(min_tokens, max_tokens)
        self.section_pattern = re.compile(section_pattern, re.MULTILINE)

    def chunk(self, text):
        # Split using section headers (like #, ##, ===)
        sections = self.section_pattern.split(text)
        
        # Reconstruct chunks with headers attached
        structured_sections = []
        for i in range(0, len(sections) - 1, 2):
            header = sections[i].strip()
            content = sections[i + 1].strip()
            structured_sections.append(f"{header}\n{content}")
        
        return self._combine_chunks(structured_sections)


# Example Usage
if __name__ == "__main__":
    text = """
# Introduction
Machine learning is a subset of artificial intelligence. It allows computers to learn from data without being explicitly programmed.

## Deep Learning
Deep learning, a subset of machine learning, uses neural networks to model complex patterns. Neural networks are composed of layers of interconnected nodes.

=== Convolutional Neural Networks
CNNs are a type of neural network designed to process grid-like data, such as images.
"""

    # Chunk by paragraph
    paragraph_chunker = ParagraphChunker(min_tokens=10, max_tokens=50)
    paragraph_chunks = paragraph_chunker.chunk(text)
    print("\n--- Paragraph Chunks ---")
    for i, chunk in enumerate(paragraph_chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")

    # Chunk by section
    section_chunker = SectionChunker()
    section_chunks = section_chunker.chunk(text)
    print("\n--- Section Chunks ---")
    for i, chunk in enumerate(section_chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")
