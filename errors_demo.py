import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch(url, tries=3):
    for attempt in range(1, tries + 1):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            print("Attempt", attempt, "failed:", e)
            time.sleep(2 * attempt)
    print("Giving up on", url)
    return None

base = "https://books.toscrape.com/catalogue/page-{}.html"
titles = []
prices = []
failed = []

for page in range(1, 51):
    url = base.format(page)
    r = fetch(url)
    if r is None:
        failed.append(url)
        continue

    soup = BeautifulSoup(r.content, "html.parser")
    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]
        price_text = book.select_one(".price_color").text
        price = float(price_text.replace("£", ""))
        titles.append(title)
        prices.append(price)

    print("Page", page, "done:", len(books), "books")
    time.sleep(0.5)

print("Books found:", len(prices))
print("Failed pages:", len(failed))
print("Total:", round(sum(prices), 2))
print("Average:", round(sum(prices) / len(prices), 2))
print("Cheapest:", min(prices))

df = pd.DataFrame({"title": titles, "price": prices})
df.to_csv("books.csv", index=False, encoding="utf-8-sig")
df.to_excel("books.xlsx", index=False)
print("Saved books.csv and books.xlsx")