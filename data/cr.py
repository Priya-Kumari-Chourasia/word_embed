import requests
from bs4 import BeautifulSoup
import os

urls = [
    "https://iitj.ac.in/bioscience-bioengineering",
    "https://iitj.ac.in/chemistry/en/chemistry",
    "https://iitj.ac.in/chemical-engineering/",
    "https://iitj.ac.in/civil-and-infrastructure-engineering/",
    "https://iitj.ac.in/computer-science-engineering/",
    "https://iitj.ac.in/electrical-engineering/",
    "https://iitj.ac.in/mathematics/",
    "https://iitj.ac.in/mechanical-engineering/",
    "https://iitj.ac.in/materials-engineering/en/materials-engineering",
    "https://iitj.ac.in/physics/",
    "https://iitj.ac.in/school-of-artificial-intelligence-data-science/en/school-of-artificial-intelligence-and-data-science",
    "https://iitj.ac.in/school-of-design/",
    "https://iitj.ac.in/school-of-liberal-arts/",
    "https://iitj.ac.in/schools/",
    "https://iitj.ac.in/cete/en/cete",
    "https://iitj.ac.in/cetsd/en/cetsd/",
    "https://iitj.ac.in/crf/en/crf",
    "https://iitj.ac.in/center-for-technology-foresight-and-policy/",
    "https://iitj.ac.in/manekshaw-centre/en/Manekshaw-Centre",
    "https://iitj.ac.in/medical-technologies/en/medical-technologies",
    "https://iitj.ac.in/rcric/"
]

def extract_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.extract()

        text = soup.get_text(separator=" ")

        # clean text
        words = [word.strip() for word in text.split()]
        text = " ".join(words)

        return text

    except Exception as e:
        print("Error scraping:", url)
        print(e)
        return ""

# create single dataset file
with open("department.txt", "w", encoding="utf-8") as outfile:

    for url in urls:
        print("Scraping:", url)

        text = extract_text(url)

        outfile.write(text)
        outfile.write("\n\n")  # separate pages

print("Scraping completed. All data saved in department.txt")