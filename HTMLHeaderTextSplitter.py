from langchain.text_splitter import HTMLHeaderTextSplitter

# Sample HTML content
html_content = """
<h1>Main Title</h1>
<p>This is the introduction paragraph under the main title.</p>
<h2>Subsection 1</h2>
<p>This is some content under subsection 1.</p>
<h2>Subsection 2</h2>
<p>This is some content under subsection 2.</p>
<h3>Sub-subsection 2.1</h3>
<p>Detailed information under sub-subsection 2.1.</p>
"""

# Define how to split based on HTML tags
headers_to_split_on = [
    ("h1", "Title"), 
    ("h2", "Section"), 
    ("h3", "Subsection")
]

# Initialize the HTMLHeaderTextSplitter
text_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# Split the HTML content
chunks = text_splitter.split_text(html_content)

# Display the result
print("Split HTML Chunks:")
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:\n{chunk}\n{'-' * 30}")
