import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def document_chunker(text, max_tokens=512, stride=256):
    """
    Chunk a document into overlapping sections similar to Semchunk's issacus function.
    
    Parameters:
    - text (str): The input document to be chunked.
    - max_tokens (int): Maximum number of tokens per chunk.
    - stride (int): Number of overlapping tokens between chunks.
    
    Returns:
    - List[str]: List of text chunks.
    """
    sentences = sent_tokenize(text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence.split())
        
        if current_length + sentence_length <= max_tokens:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            # Save current chunk
            chunks.append(' '.join(current_chunk))
            
            # Start new chunk with stride overlap
            overlap = []
            if stride > 0 and len(current_chunk) > 0:
                overlap_tokens = ' '.join(current_chunk).split()[-stride:]
                overlap = [' '.join(overlap_tokens)]
            
            current_chunk = overlap + [sentence]
            current_length = len(' '.join(current_chunk).split())
    
    # Add the final chunk if there's any leftover text
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks

# Example usage
document = """
This is an example document. It will be split into several chunks depending on the max_tokens limit. 
This helps when feeding large documents into language models that have token limits. Overlapping tokens ensure that no context is lost when moving from one chunk to another. 
This approach is particularly useful for document embeddings, summarization, and other NLP tasks.
"""

chunks = document_chunker(document, max_tokens=50, stride=25)
for idx, chunk in enumerate(chunks):
    print(f"Chunk {idx + 1}:")
    print(chunk)
    print("-" * 50)