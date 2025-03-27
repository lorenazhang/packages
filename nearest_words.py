import pdfplumber

def find_nearest_words(words, target_word, direction='right', threshold=50):
    """
    Find nearest words to the target word based on spatial distance.
    direction: 'right', 'left', 'below', 'above'
    threshold: maximum pixel distance to consider words close enough
    """
    target = next((w for w in words if target_word in w['text']), None)
    if not target:
        return []

    x0, x1, top, bottom = target['x0'], target['x1'], target['top'], target['bottom']

    nearest_words = []

    for word in words:
        if direction == 'right':
            if abs(word['top'] - top) < threshold and word['x0'] > x1:
                nearest_words.append(word)
        elif direction == 'below':
            if word['top'] > bottom and abs(word['x0'] - x0) < threshold:
                nearest_words.append(word)

    # Sort by proximity
    nearest_words.sort(key=lambda w: ((w['x0'] - x1)**2 + (w['top'] - top)**2)**0.5)

    return nearest_words

with pdfplumber.open("occ_co.pdf") as pdf:
    first_page = pdf.pages[0]
    words = first_page.extract_words()

    # 1. Find "#XXXX-XXX" (upper right)
    upper_right_number = next((w['text'] for w in words if '#' in w['text']), 'Not found')

    # 2. Find title starting with "CONSENT ORDER"
    title_word = next((w for w in words if 'CONSENT ORDER' in w['text']), None)
    title = " ".join([w['text'] for w in find_nearest_words(words, title_word['text'], direction='right', threshold=100)]) if title_word else 'Not found'
    title = title_word['text'] + " " + title if title_word else title

    # 3. Find "In the Matter of" and the text below it
    matter_word = next((w for w in words if 'In the Matter of' in w['text']), None)
    matter_words = find_nearest_words(words, matter_word['text'], direction='below', threshold=150)[:5] if matter_word else []
    matter = " ".join([w['text'] for w in matter_words]) if matter_words else 'Not found'

    # 4. Find docket number "AA-EC-XXXX-XX"
    docket_number = next((w['text'] for w in words if 'AA-EC-' in w['text']), 'Not found')

    # 5. Extract full PDF content as fallback
    full_text = "\n".join(page.extract_text() for page in pdf.pages)

print("Upper Right Number:", upper_right_number)
print("Title:", title)
print("In the Matter of:", matter)
print("Docket Number:", docket_number)
print("\nFull Text Preview:", full_text[:1000], "...")
