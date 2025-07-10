### Get rendered HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 1. Setup Selenium with headless Chrome
options = Options()
options.add_argument("--headless")  # Run without opening browser window
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# 2. Open the policy document URL
url = "https://policy.wellsfargo.com/detail/19627?anchor=4950095"  # Replace with your real URL
driver.get(url)

# 3. Wait for the JS to load and render content
time.sleep(5)  # Can be replaced with WebDriverWait for better reliability

# 4. Get the full rendered HTML
html = driver.page_source

# 5. Save to file (optional)
with open("rendered_policy.html", "w", encoding="utf-8") as f:
    f.write(html)

# 6. (Optional) Parse it with BeautifulSoup
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Example: extract all anchor blocks
anchors = soup.find_all("a", attrs={"name": True})
for a in anchors:
    print(f"Anchor ID: {a['name']} | Outer HTML: {str(a)}")

# 7. Clean up
driver.quit()


### Parse HTML
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://xxxxxx.xxxxxxxxx.com/detail/XXXXX")
time.sleep(3)

anchors = driver.find_elements(By.CSS_SELECTOR, 'a[name]')

for anchor in anchors:
    anchor_id = anchor.get_attribute("name")
    section_title = ""
    
    try:
        parent = anchor.find_element(By.XPATH, "./..")
        next_elem = parent.find_element(By.XPATH, "following-sibling::*[1]")

        if "PolicyMajorSectionHead" in next_elem.get_attribute("class"):
            section_title = next_elem.text.strip()
    except:
        continue

    print(f"Anchor: {anchor_id} | Title: {section_title}")

driver.quit()
