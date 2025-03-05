from langchain.text_splitter import RecursiveCharacterTextSplitter

# Sample large text
large_text = """
Policy 1: Data Security Guidelines
All employees must follow security protocols, including password management and encryption.

Policy 2: Remote Work Policy
Employees are allowed to work remotely under the following conditions:
1. Secure VPN must be used.
2. Data should not be stored locally.

Policy 3: Leave Policy
Employees are entitled to 20 paid leaves annually, subject to approval.
"""

# Initialize LangChain RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,     # Max characters per chunk
    chunk_overlap=20    # Overlapping context between chunks
)

# Apply chunking
chunks = text_splitter.split_text(large_text)

# Print results
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}\n{'-'*50}")
