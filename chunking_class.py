import re

class BaseChunker:
    def __init__(self, chunk_size=300, chunk_overlap=10):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def _split_large_chunks(self, chunk):
        """Split a large chunk into smaller chunks if it exceeds chunk_size."""
        tokens = chunk.split()
        chunks = []
        i = 0
        
        while i < len(tokens):
            # Take a slice of size `chunk_size`
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunks.append(' '.join(chunk_tokens))
            
            # Overlap by `chunk_overlap` tokens
            i += self.chunk_size - self.chunk_overlap

        return chunks
    
    def _combine_chunks(self, initial_chunks):
        """Handle splitting large chunks if they exceed chunk_size."""
        final_chunks = []
        
        for chunk in initial_chunks:
            if len(chunk.split()) > self.chunk_size:
                # Further split large chunks
                split_chunks = self._split_large_chunks(chunk)
                final_chunks.extend(split_chunks)
            else:
                final_chunks.append(chunk)
        
        return final_chunks


class ParagraphChunker(BaseChunker):
    def chunk(self, text):
        # First pass: Split by paragraph markers (\n\n or multiple newlines)
        paragraphs = re.split(r'\n{2,}', text.strip())
        
        # Second pass: Further split large paragraphs
        return self._combine_chunks(paragraphs)


class SectionChunker(BaseChunker):
    def __init__(self, section_pattern=r'(^#\s|^##\s|^===)', chunk_size=500, chunk_overlap=10):
        super().__init__(chunk_size, chunk_overlap)
        self.section_pattern = re.compile(section_pattern, re.MULTILINE)

    def chunk(self, text):
        # First pass: Split using section headers
        sections = self.section_pattern.split(text)
        
        # Reconstruct structured chunks with headers attached
        structured_sections = []
        for i in range(0, len(sections) - 1, 2):
            header = sections[i].strip()
            content = sections[i + 1].strip()
            structured_sections.append(f"{header}\n{content}")
        
        # Second pass: Further split large sections
        return self._combine_chunks(structured_sections)


# Example Usage
if __name__ == "__main__":
    text = """
# Introduction
Machine learning is a subset of artificial intelligence. It allows computers to learn from data without being explicitly programmed. Machine learning models improve over time as they are exposed to more data and learn from it. This ability to improve with experience makes machine learning highly useful in various applications.

## Deep Learning
Deep learning, a subset of machine learning, uses neural networks to model complex patterns. Neural networks are composed of layers of interconnected nodes, and they adjust their internal weights based on training data. Deep learning models require large amounts of data and computational power to train effectively.

=== Convolutional Neural Networks
CNNs are a type of neural network designed to process grid-like data, such as images. They use convolutional layers to identify spatial patterns and relationships. CNNs are widely used in computer vision tasks such as image classification and object detection.
"""

    # Chunk by paragraph (with overlap)
    paragraph_chunker = ParagraphChunker(chunk_size=50, chunk_overlap=5)
    paragraph_chunks = paragraph_chunker.chunk(text)
    print("\n--- Paragraph Chunks ---")
    for i, chunk in enumerate(paragraph_chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")

    # Chunk by section (with overlap)
    section_chunker = SectionChunker(chunk_size=50, chunk_overlap=5)
    section_chunks = section_chunker.chunk(text)
    print("\n--- Section Chunks ---")
    for i, chunk in enumerate(section_chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")
