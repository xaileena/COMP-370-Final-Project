import requests
import time
import csv

API_KEY = "22f2718218327e07530dc288bdbb7131"
url = "http://api.mediastack.com/v1/news"

query = "Mark Carney"
language = "en"
countries = "us,ca"
limit = 100  # max per request for free tier

offset = 0
max_articles = 100  # adjust as needed
all_articles = {}

while len(all_articles) < max_articles:
    params = {
        "access_key": API_KEY,
        "keywords": query,
        "languages": language,
        "countries": countries,
        "limit": limit,
        "offset": offset
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error: HTTP {response.status_code}")
        print("Response:", response.text)
        break
    try:
        data = response.json()
    except Exception as e:
        print("Error decoding JSON:", e)
        print("Response text:", response.text)
        break

    articles = data.get("data", [])
    if not articles:
        print("No more articles found or error:", data)
        break

    for article in articles:
        url = article.get("url")
        if url and url not in all_articles:
            all_articles[url] = article
        if len(all_articles) >= max_articles:
            break

    offset += limit
    time.sleep(1)

csv_file = "articles_mediastack.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["publishedAt", "title", "description", "url", "source_name"])
    for article in all_articles.values():
        writer.writerow([
            article.get("published_at"),
            article.get("title"),
            article.get("description"),
            article.get("url"),
            article.get("source")
        ])
