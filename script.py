import requests 
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
books_data = []

# function to extract book details 
def extract_book_details(book_url):
    res = requests.get(book_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    name = soup.find('h1').text
    price = soup.select_one(".price_color").text
    stock_status = "In Stock" if "In stock" in soup.select_one(".instock").text.strip() else "Out of Stock"
    rating = soup.select_one(".star-rating")["class"][1] # extract rating class (e.g "Three")
    category = soup.select(".breadcrumb li")[-2].text.strip() # second last breadcrumb is the category
    description = soup.select_one("#product_description ~ p").text if soup.select_one("#product_description") else "No description"

    # Extract product information table
    product_info = {}
    table_rows = soup.select(".table.table-striped tr")
    for row in table_rows:
        key = row.find("th").text.strip()
        value = row.find("td").text.strip()
        product_info[key] = value

    return {
        "Name": name,
        "Price": price,
        "Stock Status": stock_status,
        "Rating": rating,
        "Category": category,
        "Description": description,
        "Product Info": product_info
    }

# scrape the first 5 pages (each has 20 books)
for page in range(1, 6):
    url = BASE_URL.format(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    books = soup.select(".product_pod h3 a")

    for book in books:
        book_url = "https://books.toscrape.com/catalogue/" + book["href"]
        book_details = extract_book_details(book_url)
        books_data.append(book_details)

# save data to csv
df = pd.DataFrame(books_data)
df.to_csv("books_scraped.csv", index=False)

print("Scraping completed! Data saved to books_scraped.csv")
