# BrowserStack Selenium Assignment

This project uses Selenium WebDriver to scrape the first 5 opinion articles from the El País website.

Website Used:
https://elpais.com/opinion/

Features:
- Extract the first 5 opinion article links
- Open each article using Selenium
- Extract the Spanish article title
- Translate titles from Spanish to English using Google Translate
- Extract article content
- Download the cover image for each article
- Analyze repeated words in the translated titles

Technologies Used:
- Python
- Selenium WebDriver
- Requests
- Googletrans
- Collections (Counter)

Project Structure:
scraper.py – main scraping script  
requirements.txt – required Python libraries  
README.md – project documentation  

How to Run the Project:

1. Install dependencies
pip install -r requirements.txt

2. Run the scraper
python scraper.py

Output:
- Translated English titles
- Article content printed in terminal
- Images saved in the `images/` folder
- Repeated words analysis from translated titles

Author:
Siddhi Chavan