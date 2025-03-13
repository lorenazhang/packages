from bs4 import BeautifulSoup

# Example HTML policy document
html_string = """
<html>
    <head><title>Company Policy</title></head>
    <body>
        <h1>Section 1: Introduction</h1>
        <p>This policy defines the rules for conduct in the company.</p>
        <p>It applies to all employees and contractors.</p>

        <h2>1.1 Purpose</h2>
        <p>The purpose of this policy is to ensure consistency in behavior.</p>

        <h2>1.2 Scope</h2>
        <p>This policy applies to all company operations.</p>

        <h1>Section 2: Guidelines</h1>
        <p>All employees are expected to follow these guidelines:</p>
        <ul>
            <li>Be respectful to others.</li>
            <li>Follow company rules and regulations.</li>
            <li>Maintain confidentiality of company data.</li>
        </ul>

        <h1>Section 3: Enforcement</h1>
        <p>Failure to follow the policy will result in disciplinary action.</p>
    </body>
</html>
"""

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_string, 'html.parser')

# Function to extract section-wise chunks
def extract_sections(soup):
    chunks = []
    current_chunk = ""
    
    # Find all relevant tags for section breaks
    for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'li', 'ul', 'ol', 'table']):
        if tag.name in ['h1', 'h2', 'h3']:
            # When encountering a new section header, store the previous chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Start a new chunk with the heading
            current_chunk = f"{tag.get_text()}\n"
        else:
            # Append other content to the current chunk
            current_chunk += f"{tag.get_text()}\n"
    
    # Capture the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Extract and display chunks
chunks = extract_sections(soup)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:\n{chunk}\n{'-' * 40}")
