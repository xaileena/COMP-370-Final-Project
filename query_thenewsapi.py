import requests
import time
import csv

API_KEY = "API_KEY"
url = "https://api.thenewsapi.com/v1/news/all"

query = "Mark Carney"
language = "en"
page_size = 100
max_articles = 500

all_articles = {}
page = 1

while len(all_articles) < max_articles:
    params = {
        "api_token": API_KEY,
        "search": query,
        "language": language,
        "limit": page_size,
        "page": page
    }
    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("data", [])
    if not articles:
        print("No more articles found or error.")
        break

    for article in articles:
        if article["url"] not in all_articles:
            all_articles[article["url"]] = article
        if len(all_articles) >= max_articles:
            break

    page += 1
    time.sleep(1)

csv_file = "articles_thenewsapi.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["publishedAt", "title", "description", "url", "source_name"])
    for article in all_articles.values():
        writer.writerow([
            article.get("published_at"),
            article.get("title"),
            article.get("description"),
            article.get("url"),
            article.get("source") if isinstance(article.get("source"), str) else (article.get("source", {}).get("name") if isinstance(article.get("source"), dict) else None)
        ])
