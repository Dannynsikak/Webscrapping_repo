import requests
from bs4 import BeautifulSoup
import random
import pandas as pd

BASE_URL = "https://quotes.toscrape.com"
authors_data = []
visited_authors = set()

# function to extract author details
def get_author_details(author_url):
    res = requests.get(BASE_URL + author_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    name = soup.find("h3").text
    dob = soup.find("span", class_="author-born-date").text
    birthplace = soup.find("span", class_="author-born-location").text
    description = soup.find("div", class_="author-description").text.strip()

    return {
        "Name": name,
        "Date of Birth": dob,
        "Nationality": birthplace,
        "Description": description
    }

# scrape author links from multiple pages
for page in range(1, 5): # Loop through first 4 pages
    res = requests.get(f"{BASE_URL}/page/{page}")
    soup = BeautifulSoup(res.text, "html.parser")

    author_links = [a["href"] for a in soup.select(".quote .author + a")]

    for author_url in author_links:
        if author_url not in visited_authors: # Avoid duplicates
            visited_authors.add(author_url)
            author_details = get_author_details(author_url)
            authors_data.append(author_details)

        if len(authors_data) >= 20: # Limit to 20 authors
            break
    if len(authors_data) >= 20:
        break

    # save data to csv
    df = pd.DataFrame(authors_data)
    df.to_csv("authors_scraped.csv", index=False)

    print("Scraping completed! Data saved to authors_scraped.csv")