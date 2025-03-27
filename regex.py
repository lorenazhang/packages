import re
import pandas as pd


# Split the text by double newline to get individual Q&A blocks
blocks = [block.strip() for block in text.strip().split('\n\n') if block.strip()]

question_numbers = []
questions = []
answers = []

for block in blocks:
    lines = block.split('\n')
    
    # Extract question number and question
    match = re.match(r'(\d+\.\d+)\s+(.*)', lines[0])
    if match:
        q_number = match.group(1).strip()
        q_text = match.group(2).strip()
        
        # The remaining lines are the answer (joined by newline)
        ans_text = '\n'.join(lines[1:]).strip()
        
        # Store results
        question_numbers.append(q_number)
        questions.append(q_text)
        answers.append(ans_text)

# Create DataFrame
df = pd.DataFrame({
    'question number': question_numbers,
    'question': questions,
    'answer': answers
})

print(df)
---------------------------------------------------------------------

import pdfplumber

# Open the PDF file
with pdfplumber.open("occ_co.pdf") as pdf:
    first_page = pdf.pages[0]

    # Extract text from the first page
    text = first_page.extract_text()

    # 1. Extract upper right side number
    import re

    upper_right_match = re.search(r'#\d{4}-\d{3}', text)
    upper_right_number = upper_right_match.group() if upper_right_match else 'Not found'

    # 2. Extract the title
    title_match = re.search(r'(CONSENT ORDER.*?)\n', text, re.DOTALL)
    title = title_match.group(1).strip() if title_match else 'Not found'

    # 3. Extract "In the matter of"
    matter_match = re.search(r'In the Matter of:\s*(.*?)\n\)', text, re.DOTALL)
    matter = matter_match.group(1).strip().replace('\n', ' ') if matter_match else 'Not found'

    # 4. Extract docket number (AA-EC-2016-67)
    docket_match = re.search(r'AA-EC-\d{4}-\d+', text)
    docket_number = docket_match.group() if docket_match else 'Not found'

    # 5. Extract the rest of the PDF content
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

# Print the results
print("Upper Right Number:", upper_right_number)
print("Title:", title)
print("In the Matter of:", matter)
print("Docket Number:", docket_number)
print("\nFull Text:", full_text[:1000], "...")  # printing first 1000 chars for brevity
