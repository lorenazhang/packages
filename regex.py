import re
import pandas as pd

# Example input text
text = """
1.1 Question 1
answer 1

1.2, question 2
answer 2

2.1 question 3
answer 3
"""

# Define the regex pattern to match question number, question, and answer
pattern = re.compile(r'(\d+\.\d+),?\s*(.+)\n(.+?)(?=\n\d+\.\d+|\Z)', re.DOTALL)

# Find all matches using the pattern
matches = pattern.findall(text.strip())

# Create lists to store data
question_numbers = []
questions = []
answers = []

# Extract data from matches
for num, ques, ans in matches:
    question_numbers.append(num.strip())
    questions.append(ques.strip())
    answers.append(ans.strip())

# Create a DataFrame
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
