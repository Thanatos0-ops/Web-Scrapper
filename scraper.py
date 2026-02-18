# python -m pip install requests
# => get data from web (html, json, xml)

# python -m pip install beautifulsoup4
# => parse html

import csv
import json
import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "http://books.toscrape.com"

def scrape_book(url):
    response = requests.get(url)
    if(response.status_code != 200):
        return 1
    
    # Set encoding explicitly to handle special characters correctly
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")
    
    books = soup.find_all("article", class_="product_pod")
    
    all_books = []

    for book in books:
        title = book.h3.a['title']
        price_text = book.find("p", class_ = "price_color").text    
        currency = price_text[0]
        price = price_text[1:]

        all_books.append({
            "title" : title,
            "currency" : currency,
            "price" : price
        })

book = scrape_book(url)     

with open("csv_data.csv", "w", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames = ["title", "currency", "price"])
    writer.writeheader()
    writer.writerows(book)

with open("json_data.json", "w", encoding="utf_8") as f:
    json.dump(book, f, ensure_ascii=False, indent=4)
