import pandas as pd
from playwright.sync_api import sync_playwright

rows = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    n = 1

    while True:
        page.goto(f"https://quotes.toscrape.com/js/page/{n}/")
        page.wait_for_selector("div.quote")
        quotes = page.locator("div.quote")

        for i in range(quotes.count()):
            q = quotes.nth(i)
            author = q.locator("small.author").inner_text()
            text = q.locator("span.text").inner_text()
            rows.append({"author": author, "quote": text})

        print("Page", n, "done, total:", len(rows))

        if page.locator("li.next").count() == 0:
            break
        n = n + 1

    browser.close()

pd.DataFrame(rows).to_csv("quotes.csv", index=False, encoding="utf-8-sig")
print("Saved", len(rows), "quotes to quotes.csv")