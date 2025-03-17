import numpy as np
from sentence_transformers import SentenceTransformer, util

def calculate_metrics(splits, encoder):
    if len(splits) < 2:
        print("Not enough splits to calculate metrics.")
        return

    # Compute embeddings for each chunk
    embeddings = encoder.encode(splits, convert_to_tensor=True)

    # 1. Coherence Between Adjacent Chunks
    adj_coherence_scores = [
        util.pytorch_cos_sim(embeddings[i], embeddings[i + 1]).item()
        for i in range(len(embeddings) - 1)
    ]
    mean_coherence = np.mean(adj_coherence_scores)
    
    # 2. Split Boundary Quality (Similarity at Split Points)
    split_boundary_scores = [
        adj_coherence_scores[i]
        for i in range(len(adj_coherence_scores))
    ]
    mean_split_quality = np.mean(split_boundary_scores)

    # Results
    print(f"Coherence Between Adjacent Chunks: {mean_coherence:.4f}")
    print(f"Split Boundary Quality (Lower is Better): {mean_split_quality:.4f}")

    # Optional: Show all scores for debugging
    print("\nAdjacent Chunk Coherence Scores:")
    print(adj_coherence_scores)
    
    print("\nSplit Boundary Scores:")
    print(split_boundary_scores)

    return mean_coherence, mean_split_quality

# Example Usage
if __name__ == "__main__":
    # Load a lightweight embedding model
    encoder = SentenceTransformer('all-MiniLM-L6-v2')

    # Example chunks
    splits = [
        "Artificial intelligence is transforming the world.",
        "Machine learning is a subset of AI focused on pattern recognition.",
        "Deep learning uses neural networks to model complex patterns.",
        "Natural language processing allows machines to understand human language."
    ]

    # Calculate metrics
    calculate_metrics(splits, encoder)
