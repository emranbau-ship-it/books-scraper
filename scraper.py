import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

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
ratings = []
stocks = []
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
        rating_word = book.select_one("p.star-rating")["class"][1]
        rating = RATINGS[rating_word]
        stock = book.select_one(".availability").text.strip()
        titles.append(title)
        prices.append(price)
        ratings.append(rating)
        stocks.append(stock)

    print("Page", page, "done:", len(books), "books")
    time.sleep(0.5)

print("Books found:", len(prices))
print("Failed pages:", len(failed))
print("Average rating:", round(sum(ratings) / len(ratings), 2))

df = pd.DataFrame({"title": titles, "price": prices, "rating": ratings, "stock": stocks})
df.to_csv("books.csv", index=False, encoding="utf-8-sig")
df.to_excel("books.xlsx", index=False)
print("Saved books.csv and books.xlsx")

from openpyxl import load_workbook
from openpyxl.styles import Font

wb = load_workbook("books.xlsx")
ws = wb.active
ws.title = "Books"
for cell in ws[1]:
    cell.font = Font(bold=True)
ws.freeze_panes = "A2"
ws.column_dimensions["A"].width = 60
ws.column_dimensions["B"].width = 10
ws.column_dimensions["C"].width = 8
ws.column_dimensions["D"].width = 12
for cell in ws["B"][1:]:
    cell.number_format = "£0.00"
ws.auto_filter.ref = ws.dimensions
wb.save("books.xlsx")
print("Formatted books.xlsx")