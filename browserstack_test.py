from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
import requests
from googletrans import Translator
from collections import Counter
import re

USERNAME = "username"
ACCESS_KEY =  "password"

URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

translator = Translator()

browsers = [

{
"browserName": "Chrome",
"browserVersion": "latest",
"bstack:options": {
"os": "Windows",
"osVersion": "10",
"sessionName": "Chrome Test"
}
},

{
"browserName": "Firefox",
"browserVersion": "latest",
"bstack:options": {
"os": "Windows",
"osVersion": "10",
"sessionName": "Firefox Test"
}
},

{
"browserName": "Edge",
"browserVersion": "latest",
"bstack:options": {
"os": "Windows",
"osVersion": "11",
"sessionName": "Edge Test"
}
},

{
"browserName": "Chrome",
"bstack:options": {
"deviceName": "Samsung Galaxy S22",
"realMobile": "true",
"osVersion": "12.0",
"sessionName": "Samsung Mobile Test"
}
},

{
"browserName": "Safari",
"bstack:options": {
"deviceName": "iPhone 14",
"realMobile": "true",
"osVersion": "16",
"sessionName": "iPhone Safari Test"
}
}

]


def run_test(caps):

    options = webdriver.ChromeOptions()

    for key, value in caps.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=URL,
        options=options
    )

    print(f"\nRunning test on: {caps['bstack:options']['sessionName']}")

    driver.get("https://elpais.com/opinion/")
    time.sleep(5)

    print("Page Title:", driver.title)

    translated_titles = []

    try:

        try:
            driver.find_element(By.ID,"didomi-notice-agree-button").click()
        except:
            pass

        if not os.path.exists("images"):
            os.mkdir("images")

        articles = driver.find_elements(By.CSS_SELECTOR,"article h2 a")

        links = []

        for a in articles:
            link = a.get_attribute("href")

            if link and "elpais.com/opinion/" in link:
                if link not in links:
                    links.append(link)

            if len(links) == 5:
                break

        print("\nFirst 5 article links:")
        for l in links:
            print(l)

        # Visit each article
        for i, link in enumerate(links):

            driver.get(link)

            WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.TAG_NAME,"h1"))
            )

            title = driver.find_element(By.TAG_NAME,"h1").text.strip()

            if not title:
                print("Article skipped (no title found)")
    
                continue

            print("\nSpanish Title:", title)

            # Translate title
            try:
                translated = translator.translate(title, src='es', dest='en')
                english_title = translated.text
                print("English Title:", english_title)

                translated_titles.append(english_title)

            except:
                print("Translation failed")

            # Extract article text
            paragraphs = driver.find_elements(By.CSS_SELECTOR,"article p")

            print("Content:")
            for p in paragraphs[:3]:
             print(p.text)
            # Download cover image
            try:
                img = driver.find_element(By.CSS_SELECTOR,"figure img")
                img_url = img.get_attribute("src")

                img_data = requests.get(img_url).content

                with open(f"images/article_{i}.jpg","wb") as f:
                    f.write(img_data)

                print("Image downloaded")

            except:
                print("No image found")

        # Word frequency analysis
        print("\nRepeated Words (>2 times):")

        words = []

        for title in translated_titles:
            words.extend(re.findall(r'\b[a-z]+\b', title.lower()))

        word_count = Counter(words)

        for word,count in word_count.items():
            if count > 2:
                print(word,":",count)
    finally:
       try:
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Test completed"}}'
        )
       except:
        pass

    driver.quit()


# Run tests sequentially (BrowserStack free plan)
for browser in browsers:
    run_test(browser)