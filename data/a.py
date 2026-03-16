import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import PyPDF2
import io


# -------- COMMON FUNCTIONS --------

def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])

            if "iitj.ac.in" in link:
                links.append(link)

        return list(set(links))

    except:
        return []


def extract_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        return text

    except:
        return ""

"""
# -------- PROGRAMS SCRAPER --------

program_url = "https://iitj.ac.in/office-of-academics/en/academic-programs?ep=fw"

print("Collecting program category links...")

category_links = get_links(program_url)

program_pages = []

# Step 2: collect program pages from each category
for link in category_links:

    print("Scanning category:", link)

    links = get_links(link)

    program_pages.extend(links)

program_pages = list(set(program_pages))

print("Total program pages found:", len(program_pages))


with open("programs.txt","w",encoding="utf-8") as f:

    for url in program_pages:

        print("Scraping program page:", url)

        text = extract_text(url)

        if len(text) > 200:
            f.write(text)
            f.write("\n\n==== NEW PROGRAM PAGE ====\n\n")

print("Programs scraping done")


# -------- CIRCULAR SCRAPER (INCLUDING PDFs) --------

circular_url = "https://iitj.ac.in/office-of-academics/en/circulars"

circular_links = get_links(circular_url)

with open("circulars.txt","w",encoding="utf-8") as f:

    for url in circular_links:

        print("Circular:", url)

        if url.endswith(".pdf"):

            try:
                response = requests.get(url)
                pdf = PyPDF2.PdfReader(io.BytesIO(response.content))

                text = ""

                for page in pdf.pages:
                    text += page.extract_text()

                f.write(text)
                f.write("\n\n==== NEW PDF CIRCULAR ====\n\n")

            except:
                continue

        else:

            text = extract_text(url)

            if len(text) > 200:
                f.write(text)
                f.write("\n\n==== NEW CIRCULAR PAGE ====\n\n")

print("Circular scraping done")


# -------- FACULTY SCRAPER --------

faculty_main = "https://iitj.ac.in/main/en/faculty-members"

def get_department_links(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    dept_links = []

    for a in soup.find_all("a", href=True):

        link = urljoin(url, a["href"])

        if "/People/List" in link:
            dept_links.append(link)

    return list(set(dept_links))


def get_profile_links(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    profile_links = []

    for a in soup.find_all("a", href=True):

        link = urljoin(url, a["href"])

        if "/People/Profile/" in link:
            profile_links.append(link)

    return list(set(profile_links))


print("Collecting department faculty pages...")

department_pages = get_department_links(faculty_main)

print("Departments found:", len(department_pages))

profile_links = []

for dept in department_pages:

    print("Scanning department:", dept)

    links = get_profile_links(dept)

    profile_links.extend(links)


profile_links = list(set(profile_links))

print("Total faculty profiles:", len(profile_links))


with open("faculty.txt","w",encoding="utf-8") as f:

    for profile in profile_links:

        print("Scraping profile:", profile)

        text = extract_text(profile)

        if len(text) > 200:
            f.write(text)
            f.write("\n\n==== NEW FACULTY PROFILE ====\n\n")

print("Faculty scraping completed.")

"""
# -------- CURRICULUM SCRAPER --------

curriculum_url = "https://iitj.ac.in/office-of-academics/en/curriculum"

curriculum_links = get_links(curriculum_url)

with open("curriculum.txt","w",encoding="utf-8") as f:

    for url in curriculum_links:

        if url.endswith(".pdf"):

            print("Curriculum PDF:", url)

            try:
                response = requests.get(url)

                pdf = PyPDF2.PdfReader(io.BytesIO(response.content))

                text = ""

                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text

                f.write(text)
                f.write("\n\n==== NEW CURRICULUM DOCUMENT ====\n\n")

            except:
                print("Error reading PDF:", url)

print("Curriculum scraping done")