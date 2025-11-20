import requests
import time
import csv

API_KEY = "API_KEY"
url = "https://gnews.io/api/v4/search"

query = "Mark Carney"
language = "en"
countries = "us,ca"
page_size = 10
target_articles = 100

all_articles = {}
page = 1

while len(all_articles) < target_articles:
    params = {
        "q": query,
        "lang": language,
        "country": countries,
        "max": page_size,
        "apikey": API_KEY,
        "page": page
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

    articles = data.get("articles", [])
    if not articles:
        print("No more articles found or error:", data)
        break

    for article in articles:
        url = article.get("url")
        if url and url not in all_articles:
            all_articles[url] = article
        if len(all_articles) >= target_articles:
            break

    page += 1
    time.sleep(1)

csv_file = "articles_gnews.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["publishedAt", "title", "description", "url", "source_name"])
    for article in all_articles.values():
        writer.writerow([
            article.get("publishedAt"),
            article.get("title"),
            article.get("description"),
            article.get("url"),
            article.get("source", {}).get("name")
        ])