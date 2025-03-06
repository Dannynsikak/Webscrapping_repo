import requests
from bs4 import BeautifulSoup

WIKI_RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"

# Get a random Wikipedia page
res = requests.get(WIKI_RANDOM_URL)
soup = BeautifulSoup(res.text, "html.parser")

title = soup.find("h1", id="firstHeading").text
intro_paragraphs = soup.select("p")[:3]  # Get first 3 paragraphs for summary
summary = "\n".join([p.text.strip() for p in intro_paragraphs if p.text.strip()])

print(f"Title: {title}\n")
print(f"Summary:\n{summary}\n")
