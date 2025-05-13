import pandas as pd
from collections import Counter
import time

# Sample DataFrame
# df = pd.read_csv('your_data.csv')  # your real data
# df = pd.DataFrame({'desc': [...]})  # your existing df
texts = df['desc'].dropna().tolist()

# --- Your OSDS LLaMA query function ---
def query_llama(prompt):
    # Replace this with your actual endpoint call
    # Here's a fake stub for illustration
    print(f"Querying model with prompt of length {len(prompt)} chars...")
    time.sleep(1)  # simulate latency
    return "1. Management communication\n2. Workload stress\n3. Lack of career growth"

# --- Batching setup ---
batch_size = 500
seen_topics = set()
topic_counter = Counter()

# --- Process batches ---
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i + batch_size]
    
    # Include known topics in prompt to avoid repeats
    if seen_topics:
        seen_text = ", ".join(seen_topics)
        exclusion_note = f"\n\nAvoid repeating these already known topics: {seen_text}"
    else:
        exclusion_note = ""
    
    # Create prompt
    combined_text = "\n\n".join(batch_texts)
    prompt = (
        f"Given the following employee complaints, identify 3 to 5 unique high-level topics.\n"
        f"Each topic should be concise (3-5 words), without repeating prior ones.{exclusion_note}\n\n"
        f"{combined_text}\n\nList topics:"
    )

    # Query model
    try:
        response = query_llama(prompt)
        new_topics = [line.strip("1234567890. ").lower() for line in response.strip().split("\n") if line.strip()]
        
        for topic in new_topics:
            if topic not in seen_topics:
                topic_counter[topic] += 1
                seen_topics.add(topic)
                
    except Exception as e:
        print(f"Error processing batch {i // batch_size + 1}: {e}")
        continue

# --- Display top 5 topics ---
print("\nTop 5 topics across all batches:")
for topic, count in topic_counter.most_common(5):
    print(f"{topic}: {count}")
