import numpy as np
from sentence_transformers import SentenceTransformer, util
import matplotlib.pyplot as plt

class RollingWindowSplitter:
    def __init__(self, encoder, dynamic_threshold=True, min_split_tokens=100, max_split_tokens=500, window_size=2):
        self.encoder = encoder
        self.dynamic_threshold = dynamic_threshold
        self.min_split_tokens = min_split_tokens
        self.max_split_tokens = max_split_tokens
        self.window_size = window_size

    def split(self, text):
        tokens = text.split()
        num_tokens = len(tokens)
        
        # Compute embeddings for each token window
        windows = [
            ' '.join(tokens[i:i+self.window_size])
            for i in range(num_tokens - self.window_size + 1)
        ]
        embeddings = self.encoder.encode(windows, convert_to_tensor=True)

        # Compute similarity scores between adjacent windows
        similarity_scores = [
            util.pytorch_cos_sim(embeddings[i], embeddings[i + 1]).item()
            for i in range(len(embeddings) - 1)
        ]

        # Compute dynamic threshold if needed
        if self.dynamic_threshold:
            threshold = np.mean(similarity_scores) - np.std(similarity_scores)
        else:
            threshold = 0.5  # Static threshold

        splits = []
        current_chunk = []

        for i, token in enumerate(tokens):
            current_chunk.append(token)

            # If window size is exceeded, check similarity
            if len(current_chunk) >= self.window_size and i < len(similarity_scores):
                if similarity_scores[i] < threshold or len(current_chunk) >= self.max_split_tokens:
                    if len(current_chunk) >= self.min_split_tokens:
                        splits.append(' '.join(current_chunk))
                        current_chunk = []
                    else:
                        # Keep accumulating until minimum size is reached
                        continue
        
        # Add remaining chunk if it's above min_split_tokens
        if len(current_chunk) >= self.min_split_tokens:
            splits.append(' '.join(current_chunk))

        return splits, similarity_scores, threshold

    def plot_splits(self, similarity_scores, threshold, splits):
        plt.figure(figsize=(12, 8))

        # Plot similarity scores
        plt.subplot(2, 1, 1)
        plt.plot(similarity_scores, marker='o', linestyle='-', label='Similarity Scores')
        plt.axhline(y=threshold, color='green', linestyle='--', label='Threshold Similarity Score')

        for i, score in enumerate(similarity_scores):
            plt.text(i, score, f"{score:.2f}", ha='center', fontsize=8)

        # Mark split points
        split_indices = [sum(len(s.split()) for s in splits[:i]) for i in range(1, len(splits))]
        for split_index in split_indices:
            plt.axvline(x=split_index, color='red', linestyle='--')

        plt.title("Similarity Scores and Split Points")
        plt.xlabel("Document Segment Index")
        plt.ylabel("Similarity Score")
        plt.legend()

        # Plot split token sizes
        plt.subplot(2, 1, 2)
        split_sizes = [len(s.split()) for s in splits]
        plt.bar(range(len(split_sizes)), split_sizes, color='skyblue')
        for i, size in enumerate(split_sizes):
            plt.text(i, size, f"{size}", ha='center', fontsize=8)

        plt.axhline(y=self.max_split_tokens, color='red', linestyle='--', label=f'Max Split Tokens ({self.max_split_tokens})')
        plt.title("Split Token Sizes")
        plt.xlabel("Split Index")
        plt.ylabel("Token Count")
        plt.legend()

        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Load encoder
    encoder = SentenceTransformer('all-MiniLM-L6-v2')

    # Sample text (you can replace this with your actual input)
    sample_text = """
    Artificial Intelligence is the simulation of human intelligence processes by machines, especially computer systems. 
    These processes include learning (the acquisition of information and rules for using the information), reasoning 
    (using the rules to reach approximate or definite conclusions), and self-correction. AI is already significantly 
    changing the way we work and live. Machine learning, a subset of AI, enables machines to learn from data without 
    being explicitly programmed. Deep learning, a subset of machine learning, uses neural networks with many layers 
    (hence “deep” networks) to analyze large amounts of data.
    """

    # Create splitter
    splitter = RollingWindowSplitter(
        encoder=encoder,
        dynamic_threshold=True,
        min_split_tokens=20,
        max_split_tokens=50,
        window_size=2
    )

    splits, similarity_scores, threshold = splitter.split(sample_text)
    print(f"Generated {len(splits)} splits:")
    for i, split in enumerate(splits):
        print(f"Split {i + 1}:\n{split}\n")

    # Plot splits
    splitter.plot_splits(similarity_scores, threshold, splits)
