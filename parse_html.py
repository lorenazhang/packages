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
