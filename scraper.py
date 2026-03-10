from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import requests
from googletrans import Translator
from collections import Counter

# Start browser
driver = webdriver.Chrome()

translator = Translator()

# Open El Pais Opinion page
driver.get("https://elpais.com/opinion/")
time.sleep(3)

# Accept cookies if present
try:
    driver.find_element(By.ID, "didomi-notice-agree-button").click()
    time.sleep(2)
except:
    pass

# Create image folder
if not os.path.exists("images"):
    os.mkdir("images")

# Store translated titles
translated_titles = []

# -----------------------------
# Step 1: Collect first 5 article links
# -----------------------------
articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

links = []

for a in articles:
    link = a.get_attribute("href")

    if link and "elpais.com/opinion/" in link:
        if link not in links:
            links.append(link)

    if len(links) == 5:
        break

print("First 5 article links:")
for l in links:
    print(l)

# -----------------------------
# Step 2: Visit each article
# -----------------------------
for i, link in enumerate(links):

    driver.get(link)
    WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.TAG_NAME,"h1"))
)

    try:
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        title = title_element.text

        if title.strip() == "":
            print("Skipping article with empty title")
            continue

        print("\nSpanish Title:", title)

        # Translate title
        translated = translator.translate(title, src='es', dest='en')

        print("English Title:", translated.text)

        # Store translated title
        translated_titles.append(translated.text)

        # -----------------------------
        # Extract article text
        # -----------------------------
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")

        print("Content:")
        for p in paragraphs[:5]:
            print(p.text)

        # -----------------------------
        # Download cover image
        # -----------------------------
        try:
            img = driver.find_element(By.CSS_SELECTOR, "figure img")
            img_url = img.get_attribute("src")

            img_data = requests.get(img_url).content

            with open(f"images/article_{i}.jpg", "wb") as f:
                f.write(img_data)

            print("Image downloaded")

        except:
            print("No image found")

    except:
        print("Error processing article")

# -----------------------------
# Word Frequency Analysis
# -----------------------------
print("\nRepeated Words (>2 times):")

words = []

for title in translated_titles:
    words.extend(title.lower().split())

word_count = Counter(words)

for word, count in word_count.items():
    if count > 2:
        print(word, ":", count)

driver.quit()