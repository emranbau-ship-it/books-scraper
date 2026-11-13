import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
r = requests.get(url, timeout=10)
soup = BeautifulSoup(r.content, "html.parser")

books = soup.select("article.product_pod")
print("Books found:", len(books))

prices = []

for book in books:
    title = book.h3.a["title"]
    price_text = book.select_one(".price_color").text
    price = float(price_text.replace("£", ""))
    prices.append(price)
    print(title, "|", price)

print("Total:", round(sum(prices), 2))
print("Average:", round(sum(prices) / len(prices), 2))
print("Cheapest:", min(prices))