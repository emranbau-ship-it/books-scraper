import requests
from bs4 import BeautifulSoup

for url in ["https://quotes.toscrape.com/", "https://quotes.toscrape.com/js/"]:
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")
    quotes = soup.select("div.quote")
    print(url, "->", len(quotes), "quotes")