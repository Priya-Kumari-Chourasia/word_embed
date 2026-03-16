import requests
from bs4 import BeautifulSoup
import os

# pages to scrape
urls = [
    "https://iitj.ac.in/",
    "https://iitj.ac.in/m/Index/main-departments?lg=en",
    "https://iitj.ac.in/academics/index.php",
    "https://iitj.ac.in/research/",
    "https://iitj.ac.in/announcements/",
]

# create dataset folder
os.makedirs("dataset", exist_ok=True)

def clean_text(text):
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)

doc_id = 1

for url in urls:
    try:
        print("Scraping:", url)

        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        # remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        text = clean_text(text)

        # save document
        filename = f"dataset/doc_{doc_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        doc_id += 1

    except Exception as e:
        print("Error:", e)

print("Scraping finished.")